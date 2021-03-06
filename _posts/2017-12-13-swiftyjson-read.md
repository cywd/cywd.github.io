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

# 简介

[SwiftyJSON](https://github.com/SwiftyJSON/SwiftyJSON)是用`swift`写的一个`JSON`解析库。使用起来很方便，对开发者很友好。

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

现在我们就可以通过下标访问`JSON`结构体了，不过现在下标必须是枚举且明确其类型，用起来很不方便，所以我们需要设计一种更方便的方法来确定下标。

`Array`的下标是`Int`类型，而`Dictionary`的下标是`String`类型，那么我们可以实现新的`subscript`，通过参数的类型来调用相对应的实现。

首先分别实现`Int`和`String`类型参数的`subscript`，逻辑比较简单，判断类型后，如果索引是合法的则返回索引相对应元素的`JSON`结构体实例，否则生成相应的错误并赋值到空`JSON`结构然后返回。

`SwiftyJSON`定义了一个协议`JSONSubscriptType`，让`Int`和`String`都去实现该协议，这样参数的类型就统一了。然后再进行判断、调用相应的`subscript`实现

```swift
/**
 *  To mark both String and Int can be used in subscript.
 */
public enum JSONKey {
    case index(Int)
    case key(String)
}

public protocol JSONSubscriptType {
    var jsonKey: JSONKey { get }
}

extension Int: JSONSubscriptType {
    public var jsonKey: JSONKey {
        return JSONKey.index(self)
    }
}

extension String: JSONSubscriptType {
    public var jsonKey: JSONKey {
        return JSONKey.key(self)
    }
}
```

这样我们终于可以开心的以`json["name"]`这么愉快的方式来获取`JSON`内部数据了，但是如果我们来取一下内部数组的第一个元素，问题又来了，这种复杂结构的数据又应该怎么获取呢？

`SwiftyJSON`提供了两种方案，一种是以数组参数的形式，一种是不定参数列表的形式，两种方式除了参数表现形式不同，其实现逻辑是相同的。在`get`逻辑中，通过依次调用上面的`subscript`来获取最终的结果，在`set`逻辑中，如果下标个数是0直接返回，是1个通过上面的`subscript`去设置，如果多于1个，以递归的方式，逐层获取内部数据，直到剩下最后一层下标，赋值，然后返回。

```swift
/**
 Find a json in the complex data structures by using array of Int and/or String as path.

 Example:
 
 let json = JSON[data]
 let path = [9,"list","person","name"]
 let name = json[path]


 The same as: let name = json[9]["list"]["person"]["name"]

 - parameter path: The target json's path.

 - returns: Return a json found by the path or a null json with error
 */
public subscript(path: [JSONSubscriptType]) -> JSON {
    get {
        return path.reduce(self) { $0[sub: $1] }
    }
    set {
        switch path.count {
        case 0:
            return
        case 1:
            self[sub:path[0]].object = newValue.object
        default:
            var aPath = path
            aPath.remove(at: 0)
            var nextJSON = self[sub: path[0]]
            nextJSON[aPath] = newValue
            self[sub: path[0]] = nextJSON
        }
    }
}

/**
 Find a json in the complex data structures by using array of Int and/or String as path.

 - parameter path: The target json's path. Example:

 let name = json[9,"list","person","name"]

 The same as: let name = json[9]["list"]["person"]["name"]

 - returns: Return a json found by the path or a null json with error
 */
public subscript(path: JSONSubscriptType...) -> JSON {
    get {
        return self[path]
    }
    set {
        self[path] = newValue
    }
}

```
### Raw

```swift
// MARK: - Raw

extension JSON: Swift.RawRepresentable {

    public init?(rawValue: Any) {
        if JSON(rawValue).type == .unknown {
            return nil
        } else {
            self.init(rawValue)
        }
    }

    public var rawValue: Any {
        return self.object
    }

    public func rawData(options opt: JSONSerialization.WritingOptions = JSONSerialization.WritingOptions(rawValue: 0)) throws -> Data {
        guard JSONSerialization.isValidJSONObject(self.object) else {
            throw SwiftyJSONError.invalidJSON
        }

        return try JSONSerialization.data(withJSONObject: self.object, options: opt)
	}

	public func rawString(_ encoding: String.Encoding = .utf8, options opt: JSONSerialization.WritingOptions = .prettyPrinted) -> String? {
		do {
			return try _rawString(encoding, options: [.jsonSerialization: opt])
		} catch {
			print("Could not serialize object to JSON because:", error.localizedDescription)
			return nil
		}
	}

	public func rawString(_ options: [writingOptionsKeys: Any]) -> String? {
		let encoding = options[.encoding] as? String.Encoding ?? String.Encoding.utf8
		let maxObjectDepth = options[.maxObjextDepth] as? Int ?? 10
		do {
			return try _rawString(encoding, options: options, maxObjectDepth: maxObjectDepth)
		} catch {
			print("Could not serialize object to JSON because:", error.localizedDescription)
			return nil
		}
	}

	fileprivate func _rawString(_ encoding: String.Encoding = .utf8, options: [writingOptionsKeys: Any], maxObjectDepth: Int = 10) throws -> String? {
        guard maxObjectDepth > 0 else { throw SwiftyJSONError.invalidJSON }
        switch self.type {
        case .dictionary:
			do {
				if !(options[.castNilToNSNull] as? Bool ?? false) {
					let jsonOption = options[.jsonSerialization] as? JSONSerialization.WritingOptions ?? JSONSerialization.WritingOptions.prettyPrinted
					let data = try self.rawData(options: jsonOption)
					return String(data: data, encoding: encoding)
				}

				guard let dict = self.object as? [String: Any?] else {
					return nil
				}
				let body = try dict.keys.map { key throws -> String in
					guard let value = dict[key] else {
						return "\"\(key)\": null"
					}
					guard let unwrappedValue = value else {
						return "\"\(key)\": null"
					}

					let nestedValue = JSON(unwrappedValue)
					guard let nestedString = try nestedValue._rawString(encoding, options: options, maxObjectDepth: maxObjectDepth - 1) else {
						throw SwiftyJSONError.elementTooDeep
					}
					if nestedValue.type == .string {
						return "\"\(key)\": \"\(nestedString.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\""))\""
					} else {
						return "\"\(key)\": \(nestedString)"
					}
				}

				return "{\(body.joined(separator: ","))}"
			} catch _ {
				return nil
			}
        case .array:
            do {
				if !(options[.castNilToNSNull] as? Bool ?? false) {
					let jsonOption = options[.jsonSerialization] as? JSONSerialization.WritingOptions ?? JSONSerialization.WritingOptions.prettyPrinted
					let data = try self.rawData(options: jsonOption)
					return String(data: data, encoding: encoding)
				}

                guard let array = self.object as? [Any?] else {
                    return nil
                }
                let body = try array.map { value throws -> String in
                    guard let unwrappedValue = value else {
                        return "null"
                    }

                    let nestedValue = JSON(unwrappedValue)
                    guard let nestedString = try nestedValue._rawString(encoding, options: options, maxObjectDepth: maxObjectDepth - 1) else {
                        throw SwiftyJSONError.invalidJSON
                    }
                    if nestedValue.type == .string {
                        return "\"\(nestedString.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\""))\""
                    } else {
                        return nestedString
                    }
                }

                return "[\(body.joined(separator: ","))]"
            } catch _ {
                return nil
            }
        case .string:
            return self.rawString
        case .number:
            return self.rawNumber.stringValue
        case .bool:
            return self.rawBool.description
        case .null:
            return "null"
        default:
            return nil
        }
    }
}
```



### 最后结果

这样可以使用类似`json["items"][0]`这样去获取元素。不过这里有一个问题，此时获取到的元素是`JSON`结构体，我们需要把它转化成swift类型的元素。

`SwiftyJSON`通过增加一系列属性，包含了全部开发中可能的目标类型，让用户方便的获取想要类型的最终结果。如`array arrayValue string stringValue`等等，这里每种类型有两种版本。

#### 不含`Value`

如 `array, string`

如果不能把最终结果转化为对应的类型，将返回`nil`

#### 含有Value

如`arrayValue, stringValue`，如果不能把最终结果转化为对应的类型，将返回 `[]空数组` ,`""空字符串`

#### 最后

如果与属性相符则返回相应的`rowValue`，如果不相符则尝试转换或直接返回`nil`(如果是`Value`版本返回默认值).

```swift
// MARK: - Array

extension JSON {

    //Optional [JSON]
    public var array: [JSON]? {
        if self.type == .array {
            return self.rawArray.map { JSON($0) }
        } else {
            return nil
        }
    }

    //Non-optional [JSON]
    public var arrayValue: [JSON] {
        return self.array ?? []
    }

    //Optional [Any]
    public var arrayObject: [Any]? {
        get {
            switch self.type {
            case .array:
                return self.rawArray
            default:
                return nil
            }
        }
        set {
            if let array = newValue {
                self.object = array as Any
            } else {
                self.object = NSNull()
            }
        }
    }
}

// MARK: - Dictionary

extension JSON {

    //Optional [String : JSON]
    public var dictionary: [String: JSON]? {
        if self.type == .dictionary {
            var d = [String: JSON](minimumCapacity: rawDictionary.count)
            for (key, value) in rawDictionary {
                d[key] = JSON(value)
            }
            return d
        } else {
            return nil
        }
    }

    //Non-optional [String : JSON]
    public var dictionaryValue: [String: JSON] {
        return self.dictionary ?? [:]
    }

    //Optional [String : Any]

    public var dictionaryObject: [String: Any]? {
        get {
            switch self.type {
            case .dictionary:
                return self.rawDictionary
            default:
                return nil
            }
        }
        set {
            if let v = newValue {
                self.object = v as Any
            } else {
                self.object = NSNull()
            }
        }
    }
}

// MARK: - Bool

extension JSON { // : Swift.Bool

    //Optional bool
    public var bool: Bool? {
        get {
            switch self.type {
            case .bool:
                return self.rawBool
            default:
                return nil
            }
        }
        set {
            if let newValue = newValue {
                self.object = newValue as Bool
            } else {
                self.object = NSNull()
            }
        }
    }

    //Non-optional bool
    public var boolValue: Bool {
        get {
            switch self.type {
            case .bool:
                return self.rawBool
            case .number:
                return self.rawNumber.boolValue
            case .string:
                return ["true", "y", "t", "yes", "1"].contains { self.rawString.caseInsensitiveCompare($0) == .orderedSame }
            default:
                return false
            }
        }
        set {
            self.object = newValue
        }
    }
}

// MARK: - String

extension JSON {

    //Optional string
    public var string: String? {
        get {
            switch self.type {
            case .string:
                return self.object as? String
            default:
                return nil
            }
        }
        set {
            if let newValue = newValue {
                self.object = NSString(string: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    //Non-optional string
    public var stringValue: String {
        get {
            switch self.type {
            case .string:
                return self.object as? String ?? ""
            case .number:
                return self.rawNumber.stringValue
            case .bool:
                return (self.object as? Bool).map { String($0) } ?? ""
            default:
                return ""
            }
        }
        set {
            self.object = NSString(string: newValue)
        }
    }
}

// MARK: - Number

extension JSON {

    //Optional number
    public var number: NSNumber? {
        get {
            switch self.type {
            case .number:
                return self.rawNumber
            case .bool:
                return NSNumber(value: self.rawBool ? 1 : 0)
            default:
                return nil
            }
        }
        set {
            self.object = newValue ?? NSNull()
        }
    }

    //Non-optional number
    public var numberValue: NSNumber {
        get {
            switch self.type {
            case .string:
                let decimal = NSDecimalNumber(string: self.object as? String)
                if decimal == NSDecimalNumber.notANumber {  // indicates parse error
                    return NSDecimalNumber.zero
                }
                return decimal
            case .number:
                return self.object as? NSNumber ?? NSNumber(value: 0)
            case .bool:
                return NSNumber(value: self.rawBool ? 1 : 0)
            default:
                return NSNumber(value: 0.0)
            }
        }
        set {
            self.object = newValue
        }
    }
}

// MARK: - Null

extension JSON {

    public var null: NSNull? {
        get {
            switch self.type {
            case .null:
                return self.rawNull
            default:
                return nil
            }
        }
        set {
            self.object = NSNull()
        }
    }
    public func exists() -> Bool {
        if let errorValue = error, (400...1000).contains(errorValue.errorCode) {
            return false
        }
        return true
    }
}

// MARK: - URL

extension JSON {

    //Optional URL
    public var url: URL? {
        get {
            switch self.type {
            case .string:
                // Check for existing percent escapes first to prevent double-escaping of % character
                if self.rawString.range(of: "%[0-9A-Fa-f]{2}", options: .regularExpression, range: nil, locale: nil) != nil {
                    return Foundation.URL(string: self.rawString)
                } else if let encodedString_ = self.rawString.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed) {
                    // We have to use `Foundation.URL` otherwise it conflicts with the variable name.
                    return Foundation.URL(string: encodedString_)
                } else {
                    return nil
                }
            default:
                return nil
            }
        }
        set {
            self.object = newValue?.absoluteString ?? NSNull()
        }
    }
}

// MARK: - Int, Double, Float, Int8, Int16, Int32, Int64

extension JSON {

    public var double: Double? {
        get {
            return self.number?.doubleValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var doubleValue: Double {
        get {
            return self.numberValue.doubleValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var float: Float? {
        get {
            return self.number?.floatValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var floatValue: Float {
        get {
            return self.numberValue.floatValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int: Int? {
        get {
            return self.number?.intValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var intValue: Int {
        get {
            return self.numberValue.intValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt: UInt? {
        get {
            return self.number?.uintValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var uIntValue: UInt {
        get {
            return self.numberValue.uintValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int8: Int8? {
        get {
            return self.number?.int8Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: Int(newValue))
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int8Value: Int8 {
        get {
            return self.numberValue.int8Value
        }
        set {
            self.object = NSNumber(value: Int(newValue))
        }
    }

    public var uInt8: UInt8? {
        get {
            return self.number?.uint8Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt8Value: UInt8 {
        get {
            return self.numberValue.uint8Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int16: Int16? {
        get {
            return self.number?.int16Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int16Value: Int16 {
        get {
            return self.numberValue.int16Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt16: UInt16? {
        get {
            return self.number?.uint16Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt16Value: UInt16 {
        get {
            return self.numberValue.uint16Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int32: Int32? {
        get {
            return self.number?.int32Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int32Value: Int32 {
        get {
            return self.numberValue.int32Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt32: UInt32? {
        get {
            return self.number?.uint32Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt32Value: UInt32 {
        get {
            return self.numberValue.uint32Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int64: Int64? {
        get {
            return self.number?.int64Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int64Value: Int64 {
        get {
            return self.numberValue.int64Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt64: UInt64? {
        get {
            return self.number?.uint64Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt64Value: UInt64 {
        get {
            return self.numberValue.uint64Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }
}
```

## 重载操作符

```swift
// MARK: - Comparable

extension JSON: Swift.Comparable {}

public func == (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber == rhs.rawNumber
    case (.string, .string):
        return lhs.rawString == rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func <= (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber <= rhs.rawNumber
    case (.string, .string):
        return lhs.rawString <= rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func >= (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber >= rhs.rawNumber
    case (.string, .string):
        return lhs.rawString >= rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func > (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber > rhs.rawNumber
    case (.string, .string):
        return lhs.rawString > rhs.rawString
    default:
        return false
    }
}

public func < (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber < rhs.rawNumber
    case (.string, .string):
        return lhs.rawString < rhs.rawString
    default:
        return false
    }
}

private let trueNumber = NSNumber(value: true)
private let falseNumber = NSNumber(value: false)
private let trueObjCType = String(cString: trueNumber.objCType)
private let falseObjCType = String(cString: falseNumber.objCType)

// MARK: - NSNumber: Comparable

extension NSNumber {
    fileprivate var isBool: Bool {
        let objCType = String(cString: self.objCType)
        if (self.compare(trueNumber) == .orderedSame && objCType == trueObjCType) || (self.compare(falseNumber) == .orderedSame && objCType == falseObjCType) {
            return true
        } else {
            return false
        }
    }
}

func == (lhs: NSNumber, rhs: NSNumber) -> Bool {
    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == .orderedSame
    }
}

func != (lhs: NSNumber, rhs: NSNumber) -> Bool {
    return !(lhs == rhs)
}

func < (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == .orderedAscending
    }
}

func > (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == ComparisonResult.orderedDescending
    }
}

func <= (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) != .orderedDescending
    }
}

func >= (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) != .orderedAscending
    }
}

public enum writingOptionsKeys {
	case jsonSerialization
	case castNilToNSNull
	case maxObjextDepth
	case encoding
}

```



# 源码

```swift
//  SwiftyJSON.swift
//
//  Copyright (c) 2014 - 2017 Ruoyu Fu, Pinglin Tang
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in
//  all copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
//  THE SOFTWARE.

import Foundation

// MARK: - Error
// swiftlint:disable line_length
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

// MARK: - JSON Base

// JSON 结构体
public struct JSON {

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

	/**
	 Creates a JSON from JSON string
	
	 - parameter json: Normal json string like '{"a":"b"}'
	
	 - returns: The created JSON
	 */
    @available(*, deprecated, message: "Use instead `init(parseJSON: )`")
    public static func parse(_ json: String) -> JSON {
        return json.data(using: String.Encoding.utf8)
            .flatMap { try? JSON(data: $0) } ?? JSON(NSNull())
    }

	/**
	 Creates a JSON using the object.
	
	 - parameter jsonObject:  The object must have the following properties: All objects are NSString/String, NSNumber/Int/Float/Double/Bool, NSArray/Array, NSDictionary/Dictionary, or NSNull; All dictionary keys are NSStrings/String; NSNumbers are not NaN or infinity.
	
	 - returns: The created JSON
	 */
    fileprivate init(jsonObject: Any) {
        self.object = jsonObject
    }

	/**
	 Merges another JSON into this JSON, whereas primitive values which are not present in this JSON are getting added,
	 present values getting overwritten, array values getting appended and nested JSONs getting merged the same way.
 
	 - parameter other: The JSON which gets merged into this JSON
	
	 - throws `ErrorWrongType` if the other JSONs differs in type on the top level.
	 */
    public mutating func merge(with other: JSON) throws {
        try self.merge(with: other, typecheck: true)
    }

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

    /// The static null JSON
    @available(*, unavailable, renamed:"null")
    public static var nullJSON: JSON { return null }
    public static var null: JSON { return JSON(NSNull()) }
}

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

// MARK: - Subscript

/**
 *  To mark both String and Int can be used in subscript.
 */
public enum JSONKey {
    case index(Int)
    case key(String)
}

public protocol JSONSubscriptType {
    var jsonKey: JSONKey { get }
}

extension Int: JSONSubscriptType {
    public var jsonKey: JSONKey {
        return JSONKey.index(self)
    }
}

extension String: JSONSubscriptType {
    public var jsonKey: JSONKey {
        return JSONKey.key(self)
    }
}

extension JSON {

    /// If `type` is `.array`, return json whose object is `array[index]`, otherwise return null json with error.
    fileprivate subscript(index index: Int) -> JSON {
        get {
            if self.type != .array {
                var r = JSON.null
                r.error = self.error ?? SwiftyJSONError.wrongType
                return r
            } else if self.rawArray.indices.contains(index) {
                return JSON(self.rawArray[index])
            } else {
                var r = JSON.null
                r.error = SwiftyJSONError.indexOutOfBounds
                return r
            }
        }
        set {
            if self.type == .array &&
                self.rawArray.indices.contains(index) &&
                newValue.error == nil {
                self.rawArray[index] = newValue.object
            }
        }
    }

    /// If `type` is `.dictionary`, return json whose object is `dictionary[key]` , otherwise return null json with error.
    fileprivate subscript(key key: String) -> JSON {
        get {
            var r = JSON.null
            if self.type == .dictionary {
                if let o = self.rawDictionary[key] {
                    r = JSON(o)
                } else {
                    r.error = SwiftyJSONError.notExist
                }
            } else {
                r.error = self.error ?? SwiftyJSONError.wrongType
            }
            return r
        }
        set {
            if self.type == .dictionary && newValue.error == nil {
                self.rawDictionary[key] = newValue.object
            }
        }
    }

    /// If `sub` is `Int`, return `subscript(index:)`; If `sub` is `String`,  return `subscript(key:)`.
    fileprivate subscript(sub sub: JSONSubscriptType) -> JSON {
        get {
            switch sub.jsonKey {
            case .index(let index): return self[index: index]
            case .key(let key): return self[key: key]
            }
        }
        set {
            switch sub.jsonKey {
            case .index(let index): self[index: index] = newValue
            case .key(let key): self[key: key] = newValue
            }
        }
    }

	/**
	 Find a json in the complex data structures by using array of Int and/or String as path.
	
	 Example:
	

	 let json = JSON[data]
	 let path = [9,"list","person","name"]
	 let name = json[path]

	
	 The same as: let name = json[9]["list"]["person"]["name"]
	
	 - parameter path: The target json's path.
	
	 - returns: Return a json found by the path or a null json with error
	 */
    public subscript(path: [JSONSubscriptType]) -> JSON {
        get {
            return path.reduce(self) { $0[sub: $1] }
        }
        set {
            switch path.count {
            case 0:
                return
            case 1:
                self[sub:path[0]].object = newValue.object
            default:
                var aPath = path
                aPath.remove(at: 0)
                var nextJSON = self[sub: path[0]]
                nextJSON[aPath] = newValue
                self[sub: path[0]] = nextJSON
            }
        }
    }

    /**
     Find a json in the complex data structures by using array of Int and/or String as path.

     - parameter path: The target json's path. Example:

     let name = json[9,"list","person","name"]

     The same as: let name = json[9]["list"]["person"]["name"]

     - returns: Return a json found by the path or a null json with error
     */
    public subscript(path: JSONSubscriptType...) -> JSON {
        get {
            return self[path]
        }
        set {
            self[path] = newValue
        }
    }
}

// MARK: - LiteralConvertible

extension JSON: Swift.ExpressibleByStringLiteral {

    public init(stringLiteral value: StringLiteralType) {
        self.init(value as Any)
    }

    public init(extendedGraphemeClusterLiteral value: StringLiteralType) {
        self.init(value as Any)
    }

    public init(unicodeScalarLiteral value: StringLiteralType) {
        self.init(value as Any)
    }
}

extension JSON: Swift.ExpressibleByIntegerLiteral {

    public init(integerLiteral value: IntegerLiteralType) {
        self.init(value as Any)
    }
}

extension JSON: Swift.ExpressibleByBooleanLiteral {

    public init(booleanLiteral value: BooleanLiteralType) {
        self.init(value as Any)
    }
}

extension JSON: Swift.ExpressibleByFloatLiteral {

    public init(floatLiteral value: FloatLiteralType) {
        self.init(value as Any)
    }
}

extension JSON: Swift.ExpressibleByDictionaryLiteral {
    public init(dictionaryLiteral elements: (String, Any)...) {
        var dictionary = [String: Any](minimumCapacity: elements.count)
        for (k, v) in elements {
            dictionary[k] = v
        }
        self.init(dictionary as Any)
    }
}

extension JSON: Swift.ExpressibleByArrayLiteral {

    public init(arrayLiteral elements: Any...) {
        self.init(elements as Any)
    }
}

extension JSON: Swift.ExpressibleByNilLiteral {

    @available(*, deprecated, message: "use JSON.null instead. Will be removed in future versions")
    public init(nilLiteral: ()) {
        self.init(NSNull() as Any)
    }
}

// MARK: - Raw

extension JSON: Swift.RawRepresentable {

    public init?(rawValue: Any) {
        if JSON(rawValue).type == .unknown {
            return nil
        } else {
            self.init(rawValue)
        }
    }

    public var rawValue: Any {
        return self.object
    }

    public func rawData(options opt: JSONSerialization.WritingOptions = JSONSerialization.WritingOptions(rawValue: 0)) throws -> Data {
        guard JSONSerialization.isValidJSONObject(self.object) else {
            throw SwiftyJSONError.invalidJSON
        }

        return try JSONSerialization.data(withJSONObject: self.object, options: opt)
	}

	public func rawString(_ encoding: String.Encoding = .utf8, options opt: JSONSerialization.WritingOptions = .prettyPrinted) -> String? {
		do {
			return try _rawString(encoding, options: [.jsonSerialization: opt])
		} catch {
			print("Could not serialize object to JSON because:", error.localizedDescription)
			return nil
		}
	}

	public func rawString(_ options: [writingOptionsKeys: Any]) -> String? {
		let encoding = options[.encoding] as? String.Encoding ?? String.Encoding.utf8
		let maxObjectDepth = options[.maxObjextDepth] as? Int ?? 10
		do {
			return try _rawString(encoding, options: options, maxObjectDepth: maxObjectDepth)
		} catch {
			print("Could not serialize object to JSON because:", error.localizedDescription)
			return nil
		}
	}

	fileprivate func _rawString(_ encoding: String.Encoding = .utf8, options: [writingOptionsKeys: Any], maxObjectDepth: Int = 10) throws -> String? {
        guard maxObjectDepth > 0 else { throw SwiftyJSONError.invalidJSON }
        switch self.type {
        case .dictionary:
			do {
				if !(options[.castNilToNSNull] as? Bool ?? false) {
					let jsonOption = options[.jsonSerialization] as? JSONSerialization.WritingOptions ?? JSONSerialization.WritingOptions.prettyPrinted
					let data = try self.rawData(options: jsonOption)
					return String(data: data, encoding: encoding)
				}

				guard let dict = self.object as? [String: Any?] else {
					return nil
				}
				let body = try dict.keys.map { key throws -> String in
					guard let value = dict[key] else {
						return "\"\(key)\": null"
					}
					guard let unwrappedValue = value else {
						return "\"\(key)\": null"
					}

					let nestedValue = JSON(unwrappedValue)
					guard let nestedString = try nestedValue._rawString(encoding, options: options, maxObjectDepth: maxObjectDepth - 1) else {
						throw SwiftyJSONError.elementTooDeep
					}
					if nestedValue.type == .string {
						return "\"\(key)\": \"\(nestedString.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\""))\""
					} else {
						return "\"\(key)\": \(nestedString)"
					}
				}

				return "{\(body.joined(separator: ","))}"
			} catch _ {
				return nil
			}
        case .array:
            do {
				if !(options[.castNilToNSNull] as? Bool ?? false) {
					let jsonOption = options[.jsonSerialization] as? JSONSerialization.WritingOptions ?? JSONSerialization.WritingOptions.prettyPrinted
					let data = try self.rawData(options: jsonOption)
					return String(data: data, encoding: encoding)
				}

                guard let array = self.object as? [Any?] else {
                    return nil
                }
                let body = try array.map { value throws -> String in
                    guard let unwrappedValue = value else {
                        return "null"
                    }

                    let nestedValue = JSON(unwrappedValue)
                    guard let nestedString = try nestedValue._rawString(encoding, options: options, maxObjectDepth: maxObjectDepth - 1) else {
                        throw SwiftyJSONError.invalidJSON
                    }
                    if nestedValue.type == .string {
                        return "\"\(nestedString.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\""))\""
                    } else {
                        return nestedString
                    }
                }

                return "[\(body.joined(separator: ","))]"
            } catch _ {
                return nil
            }
        case .string:
            return self.rawString
        case .number:
            return self.rawNumber.stringValue
        case .bool:
            return self.rawBool.description
        case .null:
            return "null"
        default:
            return nil
        }
    }
}

// MARK: - Printable, DebugPrintable

extension JSON: Swift.CustomStringConvertible, Swift.CustomDebugStringConvertible {

    public var description: String {
        if let string = self.rawString(options: .prettyPrinted) {
            return string
        } else {
            return "unknown"
        }
    }

    public var debugDescription: String {
        return description
    }
}

// MARK: - Array

extension JSON {

    //Optional [JSON]
    public var array: [JSON]? {
        if self.type == .array {
            return self.rawArray.map { JSON($0) }
        } else {
            return nil
        }
    }

    //Non-optional [JSON]
    public var arrayValue: [JSON] {
        return self.array ?? []
    }

    //Optional [Any]
    public var arrayObject: [Any]? {
        get {
            switch self.type {
            case .array:
                return self.rawArray
            default:
                return nil
            }
        }
        set {
            if let array = newValue {
                self.object = array as Any
            } else {
                self.object = NSNull()
            }
        }
    }
}

// MARK: - Dictionary

extension JSON {

    //Optional [String : JSON]
    public var dictionary: [String: JSON]? {
        if self.type == .dictionary {
            var d = [String: JSON](minimumCapacity: rawDictionary.count)
            for (key, value) in rawDictionary {
                d[key] = JSON(value)
            }
            return d
        } else {
            return nil
        }
    }

    //Non-optional [String : JSON]
    public var dictionaryValue: [String: JSON] {
        return self.dictionary ?? [:]
    }

    //Optional [String : Any]

    public var dictionaryObject: [String: Any]? {
        get {
            switch self.type {
            case .dictionary:
                return self.rawDictionary
            default:
                return nil
            }
        }
        set {
            if let v = newValue {
                self.object = v as Any
            } else {
                self.object = NSNull()
            }
        }
    }
}

// MARK: - Bool

extension JSON { // : Swift.Bool

    //Optional bool
    public var bool: Bool? {
        get {
            switch self.type {
            case .bool:
                return self.rawBool
            default:
                return nil
            }
        }
        set {
            if let newValue = newValue {
                self.object = newValue as Bool
            } else {
                self.object = NSNull()
            }
        }
    }

    //Non-optional bool
    public var boolValue: Bool {
        get {
            switch self.type {
            case .bool:
                return self.rawBool
            case .number:
                return self.rawNumber.boolValue
            case .string:
                return ["true", "y", "t", "yes", "1"].contains { self.rawString.caseInsensitiveCompare($0) == .orderedSame }
            default:
                return false
            }
        }
        set {
            self.object = newValue
        }
    }
}

// MARK: - String

extension JSON {

    //Optional string
    public var string: String? {
        get {
            switch self.type {
            case .string:
                return self.object as? String
            default:
                return nil
            }
        }
        set {
            if let newValue = newValue {
                self.object = NSString(string: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    //Non-optional string
    public var stringValue: String {
        get {
            switch self.type {
            case .string:
                return self.object as? String ?? ""
            case .number:
                return self.rawNumber.stringValue
            case .bool:
                return (self.object as? Bool).map { String($0) } ?? ""
            default:
                return ""
            }
        }
        set {
            self.object = NSString(string: newValue)
        }
    }
}

// MARK: - Number

extension JSON {

    //Optional number
    public var number: NSNumber? {
        get {
            switch self.type {
            case .number:
                return self.rawNumber
            case .bool:
                return NSNumber(value: self.rawBool ? 1 : 0)
            default:
                return nil
            }
        }
        set {
            self.object = newValue ?? NSNull()
        }
    }

    //Non-optional number
    public var numberValue: NSNumber {
        get {
            switch self.type {
            case .string:
                let decimal = NSDecimalNumber(string: self.object as? String)
                if decimal == NSDecimalNumber.notANumber {  // indicates parse error
                    return NSDecimalNumber.zero
                }
                return decimal
            case .number:
                return self.object as? NSNumber ?? NSNumber(value: 0)
            case .bool:
                return NSNumber(value: self.rawBool ? 1 : 0)
            default:
                return NSNumber(value: 0.0)
            }
        }
        set {
            self.object = newValue
        }
    }
}

// MARK: - Null

extension JSON {

    public var null: NSNull? {
        get {
            switch self.type {
            case .null:
                return self.rawNull
            default:
                return nil
            }
        }
        set {
            self.object = NSNull()
        }
    }
    public func exists() -> Bool {
        if let errorValue = error, (400...1000).contains(errorValue.errorCode) {
            return false
        }
        return true
    }
}

// MARK: - URL

extension JSON {

    //Optional URL
    public var url: URL? {
        get {
            switch self.type {
            case .string:
                // Check for existing percent escapes first to prevent double-escaping of % character
                if self.rawString.range(of: "%[0-9A-Fa-f]{2}", options: .regularExpression, range: nil, locale: nil) != nil {
                    return Foundation.URL(string: self.rawString)
                } else if let encodedString_ = self.rawString.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed) {
                    // We have to use `Foundation.URL` otherwise it conflicts with the variable name.
                    return Foundation.URL(string: encodedString_)
                } else {
                    return nil
                }
            default:
                return nil
            }
        }
        set {
            self.object = newValue?.absoluteString ?? NSNull()
        }
    }
}

// MARK: - Int, Double, Float, Int8, Int16, Int32, Int64

extension JSON {

    public var double: Double? {
        get {
            return self.number?.doubleValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var doubleValue: Double {
        get {
            return self.numberValue.doubleValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var float: Float? {
        get {
            return self.number?.floatValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var floatValue: Float {
        get {
            return self.numberValue.floatValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int: Int? {
        get {
            return self.number?.intValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var intValue: Int {
        get {
            return self.numberValue.intValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt: UInt? {
        get {
            return self.number?.uintValue
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object = NSNull()
            }
        }
    }

    public var uIntValue: UInt {
        get {
            return self.numberValue.uintValue
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int8: Int8? {
        get {
            return self.number?.int8Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: Int(newValue))
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int8Value: Int8 {
        get {
            return self.numberValue.int8Value
        }
        set {
            self.object = NSNumber(value: Int(newValue))
        }
    }

    public var uInt8: UInt8? {
        get {
            return self.number?.uint8Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt8Value: UInt8 {
        get {
            return self.numberValue.uint8Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int16: Int16? {
        get {
            return self.number?.int16Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int16Value: Int16 {
        get {
            return self.numberValue.int16Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt16: UInt16? {
        get {
            return self.number?.uint16Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt16Value: UInt16 {
        get {
            return self.numberValue.uint16Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int32: Int32? {
        get {
            return self.number?.int32Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int32Value: Int32 {
        get {
            return self.numberValue.int32Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt32: UInt32? {
        get {
            return self.number?.uint32Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt32Value: UInt32 {
        get {
            return self.numberValue.uint32Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var int64: Int64? {
        get {
            return self.number?.int64Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var int64Value: Int64 {
        get {
            return self.numberValue.int64Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }

    public var uInt64: UInt64? {
        get {
            return self.number?.uint64Value
        }
        set {
            if let newValue = newValue {
                self.object = NSNumber(value: newValue)
            } else {
                self.object =  NSNull()
            }
        }
    }

    public var uInt64Value: UInt64 {
        get {
            return self.numberValue.uint64Value
        }
        set {
            self.object = NSNumber(value: newValue)
        }
    }
}

// MARK: - Comparable

extension JSON: Swift.Comparable {}

public func == (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber == rhs.rawNumber
    case (.string, .string):
        return lhs.rawString == rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func <= (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber <= rhs.rawNumber
    case (.string, .string):
        return lhs.rawString <= rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func >= (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber >= rhs.rawNumber
    case (.string, .string):
        return lhs.rawString >= rhs.rawString
    case (.bool, .bool):
        return lhs.rawBool == rhs.rawBool
    case (.array, .array):
        return lhs.rawArray as NSArray == rhs.rawArray as NSArray
    case (.dictionary, .dictionary):
        return lhs.rawDictionary as NSDictionary == rhs.rawDictionary as NSDictionary
    case (.null, .null):
        return true
    default:
        return false
    }
}

public func > (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber > rhs.rawNumber
    case (.string, .string):
        return lhs.rawString > rhs.rawString
    default:
        return false
    }
}

public func < (lhs: JSON, rhs: JSON) -> Bool {

    switch (lhs.type, rhs.type) {
    case (.number, .number):
        return lhs.rawNumber < rhs.rawNumber
    case (.string, .string):
        return lhs.rawString < rhs.rawString
    default:
        return false
    }
}

private let trueNumber = NSNumber(value: true)
private let falseNumber = NSNumber(value: false)
private let trueObjCType = String(cString: trueNumber.objCType)
private let falseObjCType = String(cString: falseNumber.objCType)

// MARK: - NSNumber: Comparable

extension NSNumber {
    fileprivate var isBool: Bool {
        let objCType = String(cString: self.objCType)
        if (self.compare(trueNumber) == .orderedSame && objCType == trueObjCType) || (self.compare(falseNumber) == .orderedSame && objCType == falseObjCType) {
            return true
        } else {
            return false
        }
    }
}

func == (lhs: NSNumber, rhs: NSNumber) -> Bool {
    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == .orderedSame
    }
}

func != (lhs: NSNumber, rhs: NSNumber) -> Bool {
    return !(lhs == rhs)
}

func < (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == .orderedAscending
    }
}

func > (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) == ComparisonResult.orderedDescending
    }
}

func <= (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) != .orderedDescending
    }
}

func >= (lhs: NSNumber, rhs: NSNumber) -> Bool {

    switch (lhs.isBool, rhs.isBool) {
    case (false, true):
        return false
    case (true, false):
        return false
    default:
        return lhs.compare(rhs) != .orderedAscending
    }
}

public enum writingOptionsKeys {
	case jsonSerialization
	case castNilToNSNull
	case maxObjextDepth
	case encoding
}

```



# 参考

[SwiftyJSON源代码学习](https://www.jianshu.com/p/32d4aba191b7)