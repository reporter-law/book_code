#Embedding
##功能：查数
根据整数索引查数
model.add(Embedding(1000, 64, input_length=10))
模型将输入一个大小为 (batch, input_length) 的整数矩阵。
2D转3D张量，增加了维度，即64维度
##设置参数≠输入尺寸
设置参数不在输入尺寸中找！！
设置参数1:input_dim(词汇表大小)，索引+1，与输入尺寸无关
设置参数2：output_dim(词向量维度)，查数映射维度，与输入尺寸无关
设置参数3，input_lenght = 输入尺寸的特征数，与输入尺寸有关，是输入张量的值，输入（batch_size,input_lenght)