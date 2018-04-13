#!/usr/bin/ python3
# -*-coding:utf-8-*-
"""
在实际开发中不能所有功能运行完了之后在进行测试,所以每个模块编写完成之后,应用做些测试工作
常见的测试有: 单元测试,集成,暴力测试,压力测试.

单元测试: 和程序员相关, 依赖于assert(断言)

assert断言: 断定某个条件是否满足指定内容
"""""

def div(num1, num2):
    # 断言
    assert isinstance(num1, int), "num1不是整数类型"
    assert isinstance(num2, int), "num2不是int类型"

    return num1/num2

print(div(100, 10))
# print(div("100", 20))
print (div(100, "20"))