from FlagEmbedding import BGEM3FlagModel



# model = BGEM3FlagModel('../FlagEmbedding/test_encoder_only_m3_bge-m3_sd/checkpoint-8930',  
#                        use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)



# Dense Embedding benchmark

sentences_1 = ["What are the three standards used to determine and assess the cold suitability of fuel?"]
sentences_2 = [    "|  |\n| --- |\n| ![](manual/58548175-ccef-4d6a-987c-f597b7d4d225/images/jpg/1613864587__Web.jpg) |\n| *Photo 7: Acceptable seat condition after grinding* |\n\n#### Acceptance criteria:\n\nSee service SL2022-729 Preventive grinding of exhaust valve seats. The service letter is available from MAN Energy Solutions.\n\n|  |  |\n| --- | --- |\n| The ground surface. The grindstone must have removed material from the whole width and the whole circumference of the seat. There must be no signs of blow-by.  Max. grinding depth: must not exceed the limit (G1) stated in *work card: [<a href=\"manual/58548175-ccef-4d6a-987c-f597b7d4d225/en-GB/2265-0201-0045.html\">2265-0201</a>]*. | ![](manual/58548175-ccef-4d6a-987c-f597b7d4d225/images/jpg/6920925835__en__Web.jpg) |\n\nIf the seat surface is still not acceptable when the max. grinding depth has been reached, contact MAN Energy Solutions for advice on reconditioning.\n\n![](manual/58548175-ccef-4d6a-987c-f597b7d4d225/images/jpg/9007231921428107__Web.jpg)\n\nCopyright \u00a9 2024 MAN Energy Solutions\n\n<a class=\"schema-navbar-brand\" href=\"index.html\"><img class=\"schema-navbar-logo\" src=\"manual/58548175-ccef-4d6a-987c-f597b7d4d225/assets/img/MAN_pm_pos_rgb_300.png\"/></a>\n\n\n* <a href=\"index.html\">Home</a>\n* Language\n* <a href=\"../en-GB/6907929611.html\">english</a>\n\n* <a href=\"index.html\">Home</a>",

]

embeddings_1 = model.encode(sentences_1, 
                            batch_size=12, 
                            max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
embeddings_2 = model.encode(sentences_2)['dense_vecs']
similarity = embeddings_1 @ embeddings_2.T
print(similarity)




#  Sparse Embedding benchmark


output_1 = model.encode(sentences_1, return_dense=True, return_sparse=True, return_colbert_vecs=False)
output_2 = model.encode(sentences_2, return_dense=True, return_sparse=True, return_colbert_vecs=False)


# compute the scores via lexical mathcing
lexical_scores = model.compute_lexical_matching_score(output_1['lexical_weights'][0], output_2['lexical_weights'][0])
print(lexical_scores)



