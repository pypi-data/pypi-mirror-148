from ast import literal_eval

from graphdb.schema import Node

from ingestor.common.constants import LABEL, PROPERTIES, CONTENT_ID, CC_SIMILARITY_SCORE, ALL_SIMILARITY_SCORE, \
     CONTENT_CORE_SYNOPSIS
from ingestor.content_profile.content_similarity import cluster_data_to_df, generate_new_features, \
    generate_tfidf_matrix, calculate_cosine_similarity, cluster_data_to_single_df, combine_features, create_tfidf_df, \
    calculate_single_cosine_similarity
from ingestor.content_profile.network.query_utils import QueryUtils


class SimilarityUtils:

    @staticmethod
    def add_similarity_property(list_dict_content_similarities, content_homepage_id, graph, content_label,
                                list_dataframe_homepage):

        for df in list_dataframe_homepage:
            for idx, values in df.iterrows():
                try:
                    node_to_update = Node(**{LABEL: content_label, PROPERTIES: {CONTENT_ID: int(values[CONTENT_ID])}})
                    query_content_node = graph.find_node(node_to_update)
                    if CC_SIMILARITY_SCORE not in query_content_node[0].properties:
                        existing_cc_similarity = '{}'
                    else:
                        existing_cc_similarity = query_content_node[0].properties[CC_SIMILARITY_SCORE]
                    content_similarity_property = {content_homepage_id: list_dict_content_similarities[0][values[CONTENT_ID]]}
                    updated_cc_similarity = {**literal_eval(existing_cc_similarity), **content_similarity_property}
                    print("updated cc_similarity_score {} = {}".format(values[CONTENT_ID], updated_cc_similarity))
                    graph.update_node_property(query_content_node[0], {CC_SIMILARITY_SCORE: str(updated_cc_similarity)})
                except Exception as e:
                    print(e)
                    print("Exception for content id", values[CONTENT_ID])

        return True

    @staticmethod
    def add_all_content_similarity_property(all_content_new_df, all_content_dict_cos_sim, content_label, graph):
        for idx, values in all_content_new_df.iterrows():
            try:
                node_to_update = Node(**{LABEL: content_label, PROPERTIES: {CONTENT_ID: int(values[CONTENT_ID])}})
                query_content_node = graph.find_node(node_to_update)
                print("updating all_similarity_score {} : {} ".format(values[CONTENT_ID],all_content_dict_cos_sim[values[CONTENT_ID]]))
                graph.update_node_property(query_content_node[0], {ALL_SIMILARITY_SCORE: str(all_content_dict_cos_sim[values[CONTENT_ID]])})
            except Exception as e:
                print(e)
                print("Node not available for content id:", values[CONTENT_ID])
        return True

    @staticmethod
    def add_content_similarity_all_content(content_label, graph, homepage_id):
        all_content_cluster = QueryUtils.get_all_content(content_label, graph)
        all_content_df = cluster_data_to_single_df(all_content_cluster)
        all_content_core_synopsys = QueryUtils.get_all_synopsys(CONTENT_CORE_SYNOPSIS, graph)
        all_content_new_df = combine_features(all_content_df, graph, content_label, homepage_id,
                                              all_content_core_synopsys, all_content=True)
        all_content_tfidf = create_tfidf_df(all_content_new_df)
        all_content_dict_cos_sim = calculate_single_cosine_similarity(all_content_tfidf)
        SimilarityUtils.add_all_content_similarity_property(all_content_new_df, all_content_dict_cos_sim, content_label,
                                                            graph)
        return True

    @staticmethod
    def add_content_similarity_property_based_on_homepage_id(content_label, content_homepage_id, graph):
        try:
            list_homepage_network = QueryUtils.get_contents_based_on_homepage_id(content_homepage_id, graph)

            list_dataframe_homepage = cluster_data_to_df(list_homepage_network)

            list_new_df_homepage = generate_new_features(list_dataframe_homepage, graph, content_label,
                                                         content_homepage_id)

            list_tfidf_df = generate_tfidf_matrix(list_new_df_homepage)

            list_dict_content_similarities = calculate_cosine_similarity(list_tfidf_df)

            SimilarityUtils.add_similarity_property(list_dict_content_similarities, content_homepage_id, graph,
                                                    content_label, list_dataframe_homepage)

        except Exception as e:
            print(e)
            print('Not able to add content similarity based on home page id')
        return True
