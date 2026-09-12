
import numpy


def get_dot(vec_a,vec_b):
    """计算两个向量的点积"""
    if len(vec_a) != len(vec_b):
        raise ValueError("两个向量必须维度数量相同")
    dot_sum = 0
    for a,b in zip(vec_a,vec_b):
        dot_sum += a*b
    return dot_sum

def get_norm(vec):
    """计算向量的模"""
    sum_square = 0
    for v in vec:
        sum_square += v*v

    return numpy.sqrt(sum_square)

def cos_similarity(vec_a,vec_b):
    """余弦相似度"""
    result=get_dot(vec_a,vec_b)/(get_norm(vec_b)*get_norm(vec_b))
    return result

if __name__=="__main__":
    vec_a = numpy.array([1,2,3,4,5,6,7,8,9,10])
    vec_b = numpy.array([10,9,8,7,6,5,4,3,2,1])
    print(cos_similarity(vec_a,vec_b))