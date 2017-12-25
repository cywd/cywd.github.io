---
layout: post
title: SwiftyJSON解读(4.0.0)
excerpt: "SwiftyJSON解读 版本 4.0.0"
categories: ["iOS", "源码阅读"]
tags: ["iOS", "源码阅读"]
date: 2017-12-13
comments: true
---

* TOC
{:toc}
---

# 分析

源代码都放在了`SwiftyJSON.swift`这一个文件里。

## 结构

```
1.一些错误码和 JSON type 等 枚举
2.JSON 结构体，定义了JSON的数据结构和构造方法
3.索引和集合，下标，字面值，控制台打印等基于Swift标准库协议的特性实现
4.以RowValue的形式把JSON数据转化为用户想要的数据类型
5.运算符重载实现JSON数据的比较
```

## 流程

```
1.假设我们从服务器拿到了{"description":"test"} 的一个二进制数据Data
2.把Data通过JSONSerialization反序列化后，如果没有错误发生，将得到一个Any对象，此时我们并不知道它里面具体是什么
3.把Any对象递归的解包之后，就得到了unwrapedObject，即字典
{"description":"test"}
4.根据unwrapedObject的类型，对结构体的type和rowValue赋值，以方便后续的使用
5.以object对type和rowValue进行封装，方便外部对JSON结构体数据的使用
```

## 注释

|            类型             |                    描述                    |
| :-----------------------: | :--------------------------------------: |
|           `//`            |                 普通的单行注释                  |
|          `/* */`          |                 可嵌套的多行注释                 |
|       `// MARK: -`        |                   分割线                    |
| `// TODO:` \|` // FIXME:` |              添加todo\|fixme               |
|           `///`           |  Xcode会添加该注释内容到Quick Help的Description字段  |
|         `/** */`          | 和///类似，且可以通过添加parameter、returns等字段为函数的使用提供更多的信息 |

## 访问权限

### 对于`func`

|      类型       |   文件内   | 模块(Module)内 |   其他模块   |
| :-----------: | :-----: | :---------: | :------: |
|    `open`     | 可访问和重载  |   可访问和重载    |  可访问和重载  |
|   `public`    | 可访问和重载  |   可访问和重载    | 可访问,不可重载 |
|  `internal`   | 可访问和重载  |   可访问和重载    | 不可访问和重载  |
| `fileprivate` | 可访问和重载  |   不可访问和重载   | 不可访问和重载  |
|   `private`   | 不可访问和重载 |   不可访问和重载   | 不可访问和重载  |

`final`修饰的`func`在任何地方都不能被重载（`overwrite`）

`func`默认使用`internal`

### 对于`class`

|      类型       |  文件内   | 模块(`Module`)内 |   其他模块   |
| :-----------: | :----: | :-----------: | :------: |
|    `open`     | 可访问和继承 |    可访问和继承     |  可访问和继承  |
|   `public`    | 可访问和继承 |    可访问和继承     | 可访问,不可继承 |
|  `internal`   | 可访问和继承 |    可访问和继承     | 不可访问和继承  |
| `fileprivate` | 可访问和继承 |    不可访问和继承    | 不可访问和继承  |
|   `private`   | 可访问和继承 |    不可访问和继承    | 不可访问和继承  |

`final`修饰的`class`在任何地方都不能被继承

`class`默认使用`internal`

## 错误

这些是已经过时的

```swift
/// Error domain
@available(*, deprecated, message: "ErrorDomain is deprecated. Use `SwiftyJSONError.errorDomain` instead.", renamed: "SwiftyJSONError.errorDomain")
public let ErrorDomain: String = "SwiftyJSONErrorDomain"

/// Error code
@available(*, deprecated, message: "ErrorUnsupportedType is deprecated. Use `SwiftyJSONError.unsupportedType` instead.", renamed: "SwiftyJSONError.unsupportedType")
public let ErrorUnsupportedType: Int = 999
@available(*, deprecated, message: "ErrorIndexOutOfBounds is deprecated. Use `SwiftyJSONError.indexOutOfBounds` instead.", renamed: "SwiftyJSONError.indexOutOfBounds")
public let ErrorIndexOutOfBounds: Int = 900
@available(*, deprecated, message: "ErrorWrongType is deprecated. Use `SwiftyJSONError.wrongType` instead.", renamed: "SwiftyJSONError.wrongType")
public let ErrorWrongType: Int = 901
@available(*, deprecated, message: "ErrorNotExist is deprecated. Use `SwiftyJSONError.notExist` instead.", renamed: "SwiftyJSONError.notExist")
public let ErrorNotExist: Int = 500
@available(*, deprecated, message: "ErrorInvalidJSON is deprecated. Use `SwiftyJSONError.invalidJSON` instead.", renamed: "SwiftyJSONError.invalidJSON")
public let ErrorInvalidJSON: Int = 490
```

现在的是这样

```swift
// SwiftyJSON 错误
public enum SwiftyJSONError: Int, Swift.Error {
    case unsupportedType = 999
    case indexOutOfBounds = 900
    case elementTooDeep = 902
    case wrongType = 901
    case notExist = 500
    case invalidJSON = 490
}

// SwiftyJSON 错误 extension
extension SwiftyJSONError: CustomNSError {

    /// return the error domain of SwiftyJSONError
    public static var errorDomain: String { return "com.swiftyjson.SwiftyJSON" }

    /// return the error code of SwiftyJSONError
    public var errorCode: Int { return self.rawValue }

    /// return the userInfo of SwiftyJSONError
    public var errorUserInfo: [String: Any] {
        switch self {
        case .unsupportedType:
            return [NSLocalizedDescriptionKey: "It is an unsupported type."]
        case .indexOutOfBounds:
            return [NSLocalizedDescriptionKey: "Array Index is out of bounds."]
        case .wrongType:
            return [NSLocalizedDescriptionKey: "Couldn't merge, because the JSONs differ in type on top level."]
        case .notExist:
            return [NSLocalizedDescriptionKey: "Dictionary key does not exist."]
        case .invalidJSON:
            return [NSLocalizedDescriptionKey: "JSON is invalid."]
        case .elementTooDeep:
            return [NSLocalizedDescriptionKey: "Element too deep. Increase maxObjectDepth and make sure there is no reference loop."]
        }
    }
}
```

可以看到这里只有`get`属性。

## `SwiftyJSON`中`JSON`的类型

```swift
// MARK: - JSON Type

/**
JSON's type definitions.

See http://www.json.org
*/
public enum Type: Int {
	case number
	case string
	case bool
	case array
	case dictionary
	case null
	case unknown
}
```

与`type`对应的`rawValue`，用于存储进行过类型转换后的最终结果。在`JSON`结构体里面。

```swift
/// Private object
fileprivate var rawArray: [Any] = []
fileprivate var rawDictionary: [String: Any] = [:]
fileprivate var rawString: String = ""
fileprivate var rawNumber: NSNumber = 0
fileprivate var rawNull: NSNull = NSNull()
fileprivate var rawBool: Bool = false
```

## `JSONSerialization`

`JSONSerialization`是苹果用于序列化/反序列化`JSON`数据的类，其可以实现JSON的二进制数据`Data`和`Any`对象的相互转化。由于`Data`并不一定能反序列化为`Any`对象，所以需要进行错误处理。由于得到的是`Any`类型，所以当实际使用的时候，还必须进行多次的转型和判断。

```swift
do {
  let object: Any = try JSONSerialization.jsonObject(with: data, options: [])
} catch {
  print("解析失败")
}
```

现在的`JSON`解析库基本都是基于`JSONSerialization`

## `JSON`结构体

### 初始化

从输入源考虑，有以下几种情况：

```
二进制数据Data
JSON字符串String
任意类型Any
```

虽然有多种可能的输入源，但是最终的逻辑是一样的，即通过一个解析后的`Any`对象，生成一个`JSON`结构体。我们可以把最终生成`JSON`结构体的逻辑封装成一个指定初始化方法(`Designated Initializer`)，其他的所有初始化方法则是对输入进行相应的处理后，再代理给指定初始化方法。(严格来说，指定初始化方法是作用于`Class`，相对于`Convenience Initializers`来说的，但是其思想同样可以用于`Struct`)


具体的初始化方法分析如下：

```swift
/**
 Creates a JSON using the object.

 - parameter jsonObject:  The object must have the following properties: All objects are NSString/String, NSNumber/Int/Float/Double/Bool, NSArray/Array, NSDictionary/Dictionary, or NSNull; All dictionary keys are NSStrings/String; NSNumbers are not NaN or infinity.

 - returns: The created JSON
 */
fileprivate init(jsonObject: Any) {
    self.object = jsonObject
}
```

使用这个私有方法初始化，通过参数`jsonObject`创建`JOSN`结构体实例并初始化`object`属性。`self.object = jsonObject`会去调用`object`的`set`方法。

#### 二进制数据`Data`

```swift
/**
 Creates a JSON using the data.

 - parameter data: The NSData used to convert to json.Top level object in data is an NSArray or NSDictionary
 - parameter opt: The JSON serialization reading options. `[]` by default.

 - returns: The created JSON
 */
public init(data: Data, options opt: JSONSerialization.ReadingOptions = []) throws {
    let object: Any = try JSONSerialization.jsonObject (with: data, options: opt)
    self.init(jsonObject: object)
}
```

调用系统的`JSONSerialization`对`Data`进行解析，然后执行基本初始化方法`fileprivate init(jsonObject: Any)`。

#### 任意类型Any

```swift
/**
 Creates a JSON object
 - note: this does not parse a `String` into JSON, instead use `init(parseJSON: String)`

 - parameter object: the object

 - returns: the created JSON object
 */
public init(_ object: Any) {
    switch object {
    case let object as Data:
        do {
            try self.init(data: object)
        } catch {
            self.init(jsonObject: NSNull())
        }
    default:
        self.init(jsonObject: object)
    }
}
```

因为此`Any`不一定是`JSONSerialization`解析后的`Any`，还有可能是`Data`类型。所以进行判断，如果是`Data`则执行基本初始化方法`public init(data: Data, options opt: JSONSerialization.ReadingOptions = [])`，否则执行基本初始化方法`fileprivate init(jsonObject: Any)`

#### `JSON`字符串`String`

```swift
/**
 Parses the JSON string into a JSON object

 - parameter json: the JSON string

 - returns: the created JSON object
*/
public init(parseJSON jsonString: String) {
    if let data = jsonString.data(using: .utf8) {
        self.init(data)
    } else {
        self.init(NSNull())
    }
}
```

通过字符串创建`Data`，再执行方法`public init(_ object: Any)`，如果创建失败，则通过指定初始化方法构造一个空`JSON`

### 合并(`Merge`)

除了初始化外，还提供了合并两个`JSON`结构体的方法。

方法中使用了`mutating`关键字，其作用是使得方法可以修改调用该方法的实例本身，即`self`。

#### 基本方法

```swift
/**
 Private woker function which does the actual merging
 Typecheck is set to true for the first recursion level to prevent total override of the source JSON
*/
fileprivate mutating func merge(with other: JSON, typecheck: Bool) throws {
    if self.type == other.type {
        switch self.type {
        case .dictionary:
            for (key, _) in other {
                try self[key].merge(with: other[key], typecheck: false)
            }
        case .array:
            self = JSON(self.arrayValue + other.arrayValue)
        default:
            self = other
        }
    } else {
        if typecheck {
            throw SwiftyJSONError.wrongType
        } else {
            self = other
        }
    }
}
```

方法中使用了`mutating`关键字，其作用是使得方法可以修改调用该方法的实例本身，即`self`

如果是除字典和数据外的类型，直接替换为新的数据

如果是数组，把两个数组的内容合并

如果是字典，遍历字典，如果`key`相同，递归的调用合并方法把对应的`value`进行合并，并附加一个标志`typecheck`

#### 两个结构体的type相同

```swift
/**
 Merges another JSON into this JSON, whereas primitive values which are not present in this JSON are getting added,
 present values getting overwritten, array values getting appended and nested JSONs getting merged the same way.

 - parameter other: The JSON which gets merged into this JSON

 - throws `ErrorWrongType` if the other JSONs differs in type on the top level.
 */
public mutating func merge(with other: JSON) throws {
    try self.merge(with: other, typecheck: true)
}
```

调用私有的基本合并方法

#### 两个结构体的type不同

```swift
/**
 Merges another JSON into this JSON and returns a new JSON, whereas primitive values which are not present in this JSON are getting added,
 present values getting overwritten, array values getting appended and nested JSONS getting merged the same way.

 - parameter other: The JSON which gets merged into this JSON

 - throws `ErrorWrongType` if the other JSONs differs in type on the top level.

 - returns: New merged JSON
 */
public func merged(with other: JSON) throws -> JSON {
    var merged = self
    try merged.merge(with: other, typecheck: true)
    return merged
}
```

如果`typecheck`为真说明是第一次调用，也就是说两个结构体的最外层结构是不相同的，那么无法合并，抛出定义好的`NSError`错误

如果`typecheck`为假说明是遍历字典时递归调用的，也就是说两个结构体的最外层结构是一样，只不过里层的结构不同，那么把里面的数据直接替换为新的数据

### `Private object`

```swift
/// Private object
fileprivate var rawArray: [Any] = []
fileprivate var rawDictionary: [String: Any] = [:]
fileprivate var rawString: String = ""
fileprivate var rawNumber: NSNumber = 0
fileprivate var rawNull: NSNull = NSNull()
fileprivate var rawBool: Bool = false

/// JSON type, fileprivate setter
public fileprivate(set) var type: Type = .null

/// Error in JSON, fileprivate setter
public fileprivate(set) var error: SwiftyJSONError?

```

### `Object`

```swift
/// Object in JSON
public var object: Any {
    get {
        switch self.type {
        case .array:
            return self.rawArray
        case .dictionary:
            return self.rawDictionary
        case .string:
            return self.rawString
        case .number:
            return self.rawNumber
        case .bool:
            return self.rawBool
        default:
            return self.rawNull
        }
    }
    set {
        error = nil
        switch unwrap(newValue) {
        case let number as NSNumber:
            if number.isBool {
                type = .bool
                self.rawBool = number.boolValue
            } else {
                type = .number
                self.rawNumber = number
            }
        case let string as String:
            type = .string
            self.rawString = string
        case _ as NSNull:
            type = .null
        case nil:
            type = .null
        case let array as [Any]:
            type = .array
            self.rawArray = array
        case let dictionary as [String: Any]:
            type = .dictionary
            self.rawDictionary = dictionary
        default:
            type = .unknown
            error = SwiftyJSONError.unsupportedType
        }
    }
}
```

#### get

根据`type`来判断该返回什么

#### set

把`Any`对象递归的解包之后，就得到了`unwrapedObject`

根据`unwrapedObject`的类型，对结构体的`type`和`rowValue`赋值，以方便后续的使用

以`object`对`type`和`rowValue`进行封装，方便外部对`JSON`结构体数据的使用

#### unwrap

```swift
/// Private method to unwarp an object recursively
private func unwrap(_ object: Any) -> Any {
    switch object {
    case let json as JSON:
        return unwrap(json.object)
    case let array as [Any]:
        return array.map(unwrap)
    case let dictionary as [String: Any]:
        var unwrappedDic = dictionary
        for (k, v) in dictionary {
            unwrappedDic[k] = unwrap(v)
        }
        return unwrappedDic
    default:
        return object
    }
}
```

把`Any`对象递归解包

### 一些定义

```swift
/// The static null JSON
@available(*, unavailable, renamed:"null")
public static var nullJSON: JSON { return null }
public static var null: JSON { return JSON(NSNull()) }
```

## 面向协议

对于`JSON`来说，最外层需要是`Dictionary`或者`Array`，也就是说是集合类型，所以可以把`JSON`结构体扩展为`Swift`的集合类型，即实现`Swift.Collection`协议。因为`JSON`结构体的内部数据可能为多种类型，要扩展为集合，就要先定义一种统一的索引方式。而作为索引，其本身必须是可比较的，也就是必须实现`Comparable`协议。


### `Index`和`Comparable`

```swift
public enum Index<T: Any>: Comparable {
    case array(Int)
    case dictionary(DictionaryIndex<String, T>)
    case null

    static public func == (lhs: Index, rhs: Index) -> Bool {
        switch (lhs, rhs) {
        case (.array(let left), .array(let right)):
            return left == right
        case (.dictionary(let left), .dictionary(let right)):
            return left == right
        case (.null, .null): return true
        default:
            return false
        }
    }

    static public func < (lhs: Index, rhs: Index) -> Bool {
        switch (lhs, rhs) {
        case (.array(let left), .array(let right)):
            return left < right
        case (.dictionary(let left), .dictionary(let right)):
            return left < right
        default:
            return false
        }
    }
}
```

对于`JSON`结构体来说，我们定义了7种类型，但是作为索引，只需要针对`.array`、`.dictionary`和`.null`，其他类型本身就是一个实体，没有索引的概念(`.string`本身是有索引的，不过我们不需要把字符串给拆成字符)。所以声明一个枚举，把上述三种情况统一为一个`Index`，并实现`Comparable`协议。
`Comparable`协议实际就是重载比较运算符，如`==` 、`<`等，让两个同类型的实例可以进行比较，协议的概念和实现的逻辑都比较简单：

```swift
static public func == (lhs: Index, rhs: Index) -> Bool {
    switch (lhs, rhs) {
    case (.array(let left), .array(let right)):
        return left == right
    case (.dictionary(let left), .dictionary(let right)):
        return left == right
    case (.null, .null): return true
    default:
        return false
    }
}

static public func < (lhs: Index, rhs: Index) -> Bool {
    switch (lhs, rhs) {
    case (.array(let left), .array(let right)):
        return left < right
    case (.dictionary(let left), .dictionary(let right)):
        return left < right
    default:
        return false
    }
}
```

### `Collection`

`Collection`协议可以为实现该协议的类型提供几乎全部集合常用的特性，如通过下标获取集合元素，`for…in`遍历集合元素，`count isEmpty indices`等常用属性，元素操作、距离、切片、迭代器等常用方法。


遵守`Collection`协议至少必须满足以下三点：

```
startIndex和endIndex属性用来定义元素的起始
subscript特性用来通过下标获取集合内部元素
index(after:)方法用来确定元素的排列顺序
```

理解起来也很清晰明了，一个集合通过`subscript`特性把索引和内部的元素绑定，并且确定了起始位置的索引和其他索引的后继，那么这个集合内部的元素就已经全部确定且可知的了。

而由于`Array`和`Dictionary`都已经是集合类型了，我们定义的`Index`只是通过枚举对几种情况进行了统一，那么实现协议的时候也只需要对`Index`类型进行判断，然后调用`Array`和`Dictionary`本身的相关实现即可：

```swift
public typealias JSONIndex = Index<JSON>
public typealias JSONRawIndex = Index<Any>

extension JSON: Swift.Collection {

    public typealias Index = JSONRawIndex

    public var startIndex: Index {
        switch type {
        case .array:
            return .array(rawArray.startIndex)
        case .dictionary:
            return .dictionary(rawDictionary.startIndex)
        default:
            return .null
        }
    }

    public var endIndex: Index {
        switch type {
        case .array:
            return .array(rawArray.endIndex)
        case .dictionary:
            return .dictionary(rawDictionary.endIndex)
        default:
            return .null
        }
    }

    public func index(after i: Index) -> Index {
        switch i {
        case .array(let idx):
            return .array(rawArray.index(after: idx))
        case .dictionary(let idx):
            return .dictionary(rawDictionary.index(after: idx))
        default:
            return .null
        }
    }

    public subscript (position: Index) -> (String, JSON) {
        switch position {
        case .array(let idx):
            return (String(idx), JSON(self.rawArray[idx]))
        case .dictionary(let idx):
            let (key, value) = self.rawDictionary[idx]
            return (key, JSON(value))
        default:
            return ("", JSON.null)
        }
    }
}
```

### 下标

// -----------------------------

占位

// -----------------------------

