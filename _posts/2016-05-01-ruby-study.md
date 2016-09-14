---
layout: post
title: "Ruby的学习历程"
excerpt: "Ruby的学习历程"
tags: [Git]
date: 2016-05-01 
modified: 
comments: true
---

```
#!/usr/bin/ruby -w
# -*- coding: UTF-8 -*-

puts "你好，世界";


print <<EOF

	这是第一种方式
 你好，世界
	多行字符串
EOF

print <<"TT";                # 与上面相同
    这是第二种方式创建here document 。
    多行字符串。
TT

print <<`EOC`                 # 执行命令
	echo hi there
	echo lo there
EOC

print <<"foo", <<"bar"	      # 您可以把它们进行堆叠
	I said foo.
foo
	I said bar.
bar

BEGIN {
	# 声明 code 会在程序运行之前被调用。
	puts "开始的时候执行\n\n";
}

END {
	# 声明 code 会在程序的结尾被调用。
	puts "声明 code 会在程序的结尾被调用。"
}

=begin
这也是注释

这也是注释
=end

class Sample1111
	def hello
		puts "Hello Ruby(class)";
	end
end

obj = Sample1111.new
obj.hello

class Customer111
	@@no_of_customers = 0
end

cust1 = Customer111. new
cust2 = Customer111. new


class Customer1
	@@no_of_customers = 0

	def initialize(id, name, addr)
		@cust_id = id;
		@cust_name = name;
		@cust_addr = addr;
	end
end

cust1=Customer1.new("1", "John", "Wisdom Apartments, Ludhiya")
cust2=Customer1.new("2", "Poul", "New Empire road, Khandala")

class Sample1
   def function
      statement 1
      statement 2
   end
end

# 类的实例
class CustomerMtehod 
	@@no_of_customers=0
	def initialize(id, name, addr)
		@cust_id = id;
		@cust_name = name;
		@cust_addr = addr;
	end
	def display_details()
		puts "CustomerMtehod id #@cust_id"
		puts "CustomerMtehod name #@cust_name"
		puts "CustomerMtehod addr #@cust_addr"
	end

	def total_no_of_customers()
		@@no_of_customers += 1
		puts "total_no_of_customers: #@@no_of_customers"
	end
end

cust1 = CustomerMtehod.new("1", "John", "Wisdom Apartments, Ludhiya")
cust2 = CustomerMtehod.new("2", "Poul", "New Empire road, Khandala")

cust1.display_details()
cust1.total_no_of_customers()

cust2.display_details()
cust2.total_no_of_customers()


=begin
	一般小写字母、下划线开头：变量（Variable）。
    $开头：全局变量（Global variable）。
    @开头：实例变量（Instance variable）。
    @@开头：类变量（Class variable）类变量被共享在整个继承链中
    大写字母开头：常数（Constant）。
=end

class Example1
   VAR1 = 100
   VAR2 = 200
   def show
       puts "第一个常量的值为 #{VAR1}"
       puts "第二个常量的值为 #{VAR2}"
   end
end

# 创建对象
object = Example1.new()
object.show

=begin
    self: 当前方法的接收器对象。
    true: 代表 true 的值。
    false: 代表 false 的值。
    nil: 代表 undefined 的值。
    __FILE__: 当前源文件的名称。
    __LINE__: 当前行在源文件中的编号。
=end
	
=begin
	变量 a 的值为 10，变量 b 的值为 20

	算数运算符
    + - * /   加减乘除
	% 取模，返回余数
	** 指数 变量 a 的值为 10，变量 b 的值为 20  a**b  将得到 10 的 20 次方

	比较运算符
    == != > < >= <= 
	<==> 联合比较运算符。如果第一个操作数等于第二个操作数则返回 0，如果第一个操作数大于第二个操作数则返回 1，如果第一个操作数小于第二个操作数则返回 -1。
	===  用于测试 case 语句的 when 子句内的相等。(1...10) === 5 返回 true。
	.eql? 如果接收器和参数具有相同的类型和相等的值，则返回 true。 1 == 1.0 返回 true，但是 1.eql?(1.0) 返回 false。
	equal? 如果接收器和参数具有相同的对象 id，则返回 true。如果 aObj 是 bObj 的副本，那么 aObj == bObj 返回 true，a.equal?bObj 返回 false，但是 a.equal?aObj 返回 true。
	
	赋值运算符
	= += -= *= /= %=
	**= 指数且赋值运算符，执行指数计算，并赋值给左操作数 c **= a 相当于 c = c ** a

	并行赋值
	a = 10
	b = 20
	c = 30

	使用并行赋值可以更快地声明：
	a, b, c = 10, 20, 30

	并行赋值在交换两个变量的值时也很有用：
	a, b = b, c

	逻辑运算符
	and  称为逻辑与运算符。如果两个操作数都为真，则条件为真。	
	or   称为逻辑或运算符。如果两个操作数中有任意一个非零，则条件为真。
	&&   称为逻辑与运算符。如果两个操作数都非零，则条件为真。
	||   称为逻辑或运算符。如果两个操作数中有任意一个非零，则条件为真。
	!    称为逻辑非运算符。用来逆转操作数的逻辑状态。如果条件为真则逻辑非运算符将使其为假。
	not  称为逻辑非运算符。用来逆转操作数的逻辑状态。如果条件为真则逻辑非运算符将使其为假。
	!和not作用相同

	三元运算符
	? :	   条件表达式


	范围运算符
	..    创建一个从开始点到结束点的范围（包含结束点） 1..10 创建从 1 到 10 的范围
	...   创建一个从开始点到结束点的范围（不包含结束点） 1...10 创建从 1 到 9 的范围


	defined? 运算符
	defined? variable # 如果 variable 已经初始化，则为 True

	foo = 42
	defined? foo    # => "local-variable"
	defined? $_     # => "global-variable"
	defined? bar    # => nil（未定义） 

	defined? method_call # 如果方法已经定义，则为 True
	defined? puts        # => "method"
	defined? puts(bar)   # => nil（在这里 bar 未定义）
	defined? unpack      # => nil（在这里未定义）

=end


# if  a == 4 then a == 7 end

x=1
if x > 2
   puts "x 大于 2"
elsif x <= 2 and x!=0
   puts "x 是 1"
else
   puts "无法得知 x 的值"
end

$debug = 1
print "debug\n" if $debug

x = 1
unless x > 2
   puts "x 小于 2"
 else
  puts "x 大于 2"
end

$var =  1
print "1 -- 这一行输出\n" if $var
print "2 -- 这一行不输出\n" unless $var

$var = false
print "3 -- 这一行输出\n" unless $var


# when a == 4 then a = 7 end
# case expr0
# when expr1, expr2
# 	stmt1
# when expr3, expr4
# 	stmt2
# else
# 	stmt3
# end

# _tmp = expr0
# if expr1 === _tmp || expr2 === _tmp
#    stmt1
# elsif expr3 === _tmp || expr4 === _tmp
#    stmt2
# else
#    stmt3
# end

$age =  5
case $age
when 0 .. 2
    puts "婴儿"
when 3 .. 6
    puts "小孩"
when 7 .. 12
    puts "child"
when 13 .. 18
    puts "少年"
else
    puts "其他年龄段的"
end
# 输出小孩

foo = false
bar = true
quu = false

case
when foo then puts 'foo is true'
when bar then puts 'bar is true'
when quu then puts 'quu is true'
end
# 显示 "bar is true"


# 循环

$i = 0
$num = 5

while $i < $num do
	puts("在循环语句中 i = #$i" )
   $i +=1	
end

$i = 0
$num = 5
begin
   puts("在循环语句中 i = #$i" )
   $i +=1
end while $i < $num

$i = 0
$num = 5

until $i > $num  do
   puts("在循环语句中 i = #$i" )
   $i +=1;
end

$i = 0
$num = 5
begin
   puts("在循环语句中 i = #$i" )
   $i +=1;
end until $i > $num


# for
for i in 0..5
	puts "局部变量的值为 #{i}"
end

# 等价于
(0..5).each do |i|
   puts "局部变量的值为 #{i}"
end

for i in 0..5
   if i > 2 then
      break
   end
   puts "局部变量的值为 #{i}"
end

for i in 0..5
   if i < 2 then
   	  # 类似c语言的continue
      next
   end
   puts "局部变量的值为 #{i}"
end

# for i in 0..5
#    if i < 2 then
#       puts "局部变量的值为 #{i}"
#       redo
#    end
# end

=begin
	retry
	如果 retry 出现在 begin 表达式的 rescue 子句中，则从 begin 主体的开头重新开始。
	begin
	   do_something   # 抛出的异常
	rescue
	   # 处理错误
	   retry          # 重新从 begin 开始
	end

	for i in 1..5
	   retry if some_condition # 重新从 i == 1 开始
	end
=end

# for i in 1..5
#    retry if  i > 2
#    puts "局部变量的值为 #{i}"
# end

def testMethod(a1 = "Ruby", a2 = "Perl")
	puts "编程语言 #{a1}"
	puts "编程语言 #{a2}"
end

testMethod("c", "C++")
testMethod "c", "C++"
testMethod "c"
testMethod()
testMethod

def test1111
	i = 100
	j = 10
	k = 0
return i, j, k;
end

var = test1111
puts var

def sample (*test)
   puts "参数个数为 #{test.length}"
   for i in 0...test.length
      puts "参数值为 #{test[i]}"
   end
end
sample "Zara", "6", "F"
sample "Mac", "36", "M", "MCA"

# alias 定义别名
alias tt test1111 
puts tt

# undef 这个语句用于取消方法定义。undef 不能出现在方法主体内。
undef tt
# puts tt


# 代码块的使用
def yieldTest
	puts "你在 yieldTest 方法内"

	yield
		puts "你又回到了 yieldTest 方法内"
	yield
end

yieldTest {puts "你在代码块内"}

def test_yield_num
	puts "在 test1 方法内"
	yield 5
	puts "在 test2 方法内"
	puts "在 test3 方法内"
	yield 100
	puts "在 test4 方法内"
end
test_yield_num {|i| puts "你在块 #{i} 内"}


def test_block(&block)
   block.call
end

test_block { puts "Hello Wisdom" }

# BEGIN END 代码块
BEGIN { 
  # BEGIN 代码块
  puts "BEGIN 代码块"
} 

END { 
  # END 代码块
  puts "END 代码块"
}
  # MAIN 代码块
puts "MAIN 代码块"


# Ruby 模块（Module）

# 定义在 Test1.rb 文件中的模块
module Trig
   PI = 3.141592654
   def Trig.sin(x)
   # ..
   end
   def Trig.cos(x)
   # ..
   end
end

# require '' 用来引入文件


# Ruby string
# Ruby 字符串分为单引号字符串（'）和双引号字符串（"），区别在于双引号字符串能够支持更多的转义字符。
name1 = "Joe"
name2 = "Mary"
puts "你好 #{name1},  #{name2} 在哪?"

x, y, z = 12, 36, 72
puts "x 的值为 #{ x }"
puts "x + y 的值为 #{ x + y }"
puts "x + y + z 的平均值为 #{ (x + y + z)/3 }"


myStr = String.new("THIS IS TEST")
foo = myStr.downcase

puts "#{foo}"


# Ruby array
names = Array.new
names = Array.new(20)
puts "#{names}"
puts names.size  # 返回 20
puts names.length # 返回 20

names = Array.new(4, "mac")

puts "#{names}" # 以字符串的方式打印names
puts names # 直接打印数组

nums = Array.new(10) { |e| e = e * 2 }

puts "#{nums}"

nums = Array.[](1, 2, 3, 4, 5)
puts "#{nums}"








































```


