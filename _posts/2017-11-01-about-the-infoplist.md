---
layout: post
title: 关于info.plist
excerpt: "plist的一些字段简介"
categories: [iOS]
tags: [iOS]
date: 2017-11-01
comments: true
---

* TOC
{:toc}
---

Info.plist用于向iOS提供关于app，bundle或者framework的一些重要信息。它指定了比如一个应用应该怎样启动，它如何被本地化，应用的名称，要显示的图标，还有更多。Info.plist文件实际上是苹果预定义schema的XML文件。

    为了构建一个设备相关的健，你在健的后面要加上~iphone或者~ipad。

 

## **常用字段:**

------

###   1.获取版本信息:

    NSDictionary*infoDic = [[NSBundle mainBundle] infoDictionary];

    NSString *localVersion = [infoDic objectForKey:@"CFBundleShortVersionString"];

###   2.应用支持http网络请求:

    在Info.plist中添加 NSAppTransportSecurity 类型 Dictionary 。
    在 NSAppTransportSecurity 下添加 NSAllowsArbitraryLoads 类型Boolean ,值设为 YES

    注意类型NSAppTransportSecurity为Dictionary，NSAllowsArbitraryLoads为Boolean，复制粘贴的时候，不要多了空格，segment fault 页面上直接复制，经常会多一个出空格！

## **控制应用的名称:**

------

 **表A-1 控制应用的名称**

| 字段                  | 类型     | 是否必须 | 摘要                                       |
| ------------------- | ------ | ---- | ---------------------------------------- |
| CFBundleName        | String | Yes  | bundle的简称, 这个健指定了你的应用的名称                 |
| CFBundleDisplayName | String | No   | 本地化的bundle名, 本地化，可以通过InfoPlist.strings文件来为每个语言指定一个合适的值 |

 

**CFBundleDisplayName**

****

CFBundleDisplayName字段指定了一个字符串值来标识bundle的显示名称。Finder和其他用户界面组件会把它显示给用户。这个名 称可以与文件系统中的bundle名不同。通过把字段加入适当的.lproj子目录中的InfoPlist.strings文件，就可以实现该字段的本地 化。如果您需要本地化这个字段，您还应该提供一个CFBundleName字段的本地化版本。

 

****

### CFBundleName

CFBundleName指定了该bundle的简称。简称应该小于16个字符并且适合在菜单和“关于”中显示。通过把它加入到适当的.lproj子文件 夹下的InfoPlist.strings文件中，该字段可以被本地化。如果您本地化了该字段，那您也应该提供一个 CFBundleDisplayName字段的本地化版本。

## **应用标识+应用版本:**

------

 **表A-2应用标识+应用版本**

| 字段                         | 类型     | 是否必须 | 摘要                                       |
| -------------------------- | ------ | ---- | ---------------------------------------- |
| CFBundleIdentifier         | String | YES  | 该bundle的唯一标识字符串。该字符串的格式类似java包的命名方式，例如：com.apple.myapp。 |
| CFBundleShortVersionString | String | YES  | 这个值是一个字符串，用来指定你在APP Store上面看的的版本号，这个值必须在每一次App Store发布版本中递增 |
| CFBundleVersion            | String | YES  | 可执行文件的创建号,  这个健的值是一个证书，你可以在每一次发布时增加它。    |

### CFBundleIdentifier

CFBundleIdentifier字段指定了bundle的一个唯一的标识字符串。该标识符采用了类似Java包的命名方式，例如com.apple.myapp。该bundle标识符可以在运行时定位bundle。预置系统使用这个字符串来唯一地标识每个应用程序。

   

它包含一个唯一标识的字符串，它是从你在iOS Provisioning Portal创建的App ID取得的 App ID包含两个部分：Team ID和Bundle ID

### CFBundleShortVersionString

CFBundleShortVersionString字段指定了bundle的版本号。一般包含该bundle的主、次版本号。这个字符串的格式通常是 “n.n.n”（n表示某个数字）。第一个数字是bundle的主要版本号，另两个是次要版本号。该字段的值会被显示在Cocoa应用程序的关于对话框 中。

   

该字段不同于CFBundleVersion，它指定了一个特殊的创建号。而CFBundleShortVersionString的值描述了一种更加正式的并且不随每一次创建而改变的版本号。

**CFBundleVersion**

****

CFBundleVersion字段指定了一个字符串用来标识创建号。该字段的值通常随每一次创建而改变，并且会被显示在Cocoa”关于”对话框中的扩号里。

    为了指定一个发布版的bundle的版本信息，可以使用CFBundleShortVersionString字段。参见“CFBundleShortVersionString”。

****

## **获取用户权限信息:**

------

  用来访问用户信息的Reason strings  iOS6中需要从用户那里得到授权的数据

 //Calendars,Contacts Location,Photos,Reminders

****

**表A-3 获取用户权限信息**

****

****

| 字段                             | 类型     | 是否必须 | 摘要                                       |
| ------------------------------ | ------ | ---- | ---------------------------------------- |
| NSCalendarsUsageDescription    | String | No   | 当应用第一次视图访问用户的日历的时候，会出现一个弹出框来向用户请求权限。如果你对这个键设置了一个值，那么这个值将会显示在弹出框中 |
| NSContactsUsageDescription     | String | No   | 应用第一次尝试访问用户的通讯录的时候，会出现一个弹出框申请权限。就像是前一个键，你对这个键指定的值，将会显示在弹出框中 |
| NSPhotoLibraryUsageDescription | String | No   | 同上,照片                                    |
| NSRemindersUsageDescription    | String | No   | 同上,备忘录                                   |
| NSLocationUsageDescription     | String | No   | 同上,位置信息                                  |

 

****

****

## **应用图标:**

------

****

**表A-4 应用图标**

****

| 字段                 | 类型           | 是否必须 | 摘要                                       |
| ------------------ | ------------ | ---- | ---------------------------------------- |
| CFBundleIconFile   | String       | No   | 图标文件的文件名- 在3.2版本被废弃                      |
| UIPrerendered Icon | Boolean      | No   | 这个键自从第一个iOS SDK就有了，它告诉iOS是否给你应用的图标添加光照效果 |
| CFBundleIconFiles  | Array        | No   | 这个键的引入，是用来处理在iPad和retina屏幕的出现时，所需图标数量的增长的。这个健的值应该是一个字符串数组 -在5.0版本被废弃CFBundleExecutable |
| CFBundleIcons      | NSDictionary | No   | 这个健是iOS 5.0增加的，可以让开发者指定Newsstand图标和普通应用的图标 |

### CFBundleIconFile

CFBundleIconFile字段指定了包含该bundle图标的文件。您给出的文件名不需要包含“.icns”扩展名。Finder会在该bundle的“Resource”文件夹内寻找图标文件。

如果您的bundle使用了自定义的图标，那您就必须指定该属性。假如您没有指定，Finder（和其他应用程序）会使用缺省的图标来显示您的bundle。

****

## **控制应用初始化启动:**

------

 **表A-5 控制应用初始化启动**

****

| 字段                   | 类型     | 是否必须 | 摘要                                       |
| -------------------- | ------ | ---- | ---------------------------------------- |
| UILaunchImageFile    | String | No   | 启动图片                                     |
| NSMainNibFile        | String | No   | 应用程序的主nib文件名, 如果你用NIB的话，这个就是一个很重要的键。它指定了当你应用启动的时候，用于创建初始化窗口和相关对象的NIB文件 |
| UIMainStoryboardFile | String | No   | 如果你用Storyboard的话，这是一个很重要的键。它指定可一个storyboard文件，用于在应用启动的时候创建初始界面 |

### NSMainNibFile

NSMainNibFile字段包含了一个含有应用程序的主nib文件名（不包含.nib文件扩展名）的字符串。一个nib文件作为一个 Interface Builder的存档文件，含有对用户界面的详细描述信息以及那些界面中的对象之间的关联信息。当应用程序被启动时，主nib文件会被自动装载。Mac OS X会寻找与应用程序名相匹配的nib文件。

## **用户界面:**

------

**表A-6  用户界面**

****

| 字段                               | 类型           | 是否必须 | 摘要                                       |
| -------------------------------- | ------------ | ---- | ---------------------------------------- |
| UISupportedInterfaceOrientations | Array        | No   | 这个键的值是一个你应用支持的屏幕方向的数组                    |
| UIInterfaceOrientation           | String       | No   | 如果你的应用值支持一个方向，那么你应该设置这个键。它保证在你应用启动的时候，状态栏在正确的方向，而不是启动的时候在一个方向，然后又通过动画移动到另外一个方向。 |
| UIStatusBarStyle                 | String       | No   | 设置应用启动时状态栏的初始风格                          |
| UIStatusBarHidden                | BOOL         | No   | 这个键表示，在应用启动的时候，状态栏是否隐藏。                  |
| UIStatusBarTintParameters        | NSDictionary | No   | 状态栏可以进行一些美化                              |

UISupportedInterfaceOrientations

这个键的值是一个你应用支持的屏幕方向的数组。可用选项有：

   UIInterfaceOrientationPortrait：Home键在下方的竖屏模式

   UIInterfaceOrientationPortraitUpsideDown：Home键在上方的竖屏模式

   UIInterfaceOrientationLandscapeLeft：Home键在左方的竖屏模式

   UIInterfaceOrientationLandscapeRight：Home键在右方的竖屏模式

UIStatusBarStyle

 这个键设置应用启动时状态栏的初始风格。UIStatusBarStyle的枚举值：

   UIStatusBarStyleDefault、UIStatusBarStyleBlackTranslucent、

 UIStatusBarStyleBalackOpaque

UIStatusBarTintParameters

在iOS6中状态栏可以进行一些美化,在这个字典中又四个键：

  Style：表示导航条的barStyle属性

  Translucent：表示导航条的translucent属性

  TintColor：这个指定了导航条的修饰颜色。

  groundImage：如果你的导航条有背景图片，那么在这里把图片的文件名写上。

## **应用控制:**

------

 **表A-7 应用控制**

| 字段                                    | 类型               | 是否必须 | 摘要                                       |
| ------------------------------------- | ---------------- | ---- | ---------------------------------------- |
| UIRequiredDeviceCapabilities          | Array/Dictionary | No   | 它能让你指定设备必须要有的特性，或者设备必须不能有的特性             |
| UIBackgroundModes                     | Array            | No   | 当你需要你的应用在后台运行时，就需要这个后台模式,数组里包含应用需要的所有后台模式 |
| MKDirectionsApplicationSupportedModes | Array            | No   | 这个iOS6新增加的一个键。它允许你为特定的区域和交通模式指定你的应用的路由信息 |
| UIDeviceFamily                        | Number/Array     | No   | Xcode自动添加这个键，所以你不需要自己添加。它表示应用支持哪些设备CFBundleGetInfoHTML |
| UIAppFonts                            | Array            | No   | 如果你需要额外的字体。这个键可以为你的应用添加非标准的字体            |
| UIApplicationExitsOnSuspend           | Boolean          | No   | 如果这个键设置为true，那么应用将会直接中断，而不是切换到后台         |
| UIFileSharingEnabled                  | Boolean          | No   | 如果你希望用户能用iTunes的文件共享功能将文件从你的应用的document目录传入或传出，那么你需要设置这个键的值为true |
| UINewsstandApp                        | Boolean          | No   | 如果 你的应用时Newsstand类型的，那么你应该将这个键设置为true    |
| UIRequiresPersistentWiFi              | Boolean          | No   | iOS在默认情况下，如果设备30分钟没有活动，它就会关闭WiFi连接。如果你设置这个键的值为true，那么这个行为会被覆盖，只要你的应用是打开的，网络连接就不会关闭 |
| UISupportedExternalAccessoryProtocols | Array            | No   | 这个键指定了和附加的硬件设备通讯的协议                      |

****

UIBackgroundModes

当你需要你的应用在后台运行时，就需要这个后台模式,数组里包含应用需要的所有后台模式，可以从以下几个值里面
    选择：
    audio：使用音频框架来播放或者录制音频
    location：需要在后台访问用户的位置信息
    voip：这个应用支持IP语音，需要在后台进行Internet连接和音频播放
    newsstand-content：使用Newsstand API在后台下载并处理内容，这允许当一个代表有新的可用发布的推送
    发进来的时候唤醒应用
    external-accessory：使用External Accessory框架来和外部的设备惊醒通讯

    bluetooth-central：使用CoreBluetooth框架和外部设备进行通讯

****

## **高级视图控制:**

------

 **表A-8 高级视图控制**

| 字段                     | 类型      | 是否必须 | 摘要                                       |
| ---------------------- | ------- | ---- | ---------------------------------------- |
| UIViewEdgeAntialiasing | Boolean | No   | 默认情况下，你的视图被iOS的渲染系统绘制，不包括反锯齿功能。这是因为不是用反锯齿运行速度会快很多 |
| UIViewGroupOpacity     | Boolean | No   | 当你设置了视图的透明度，它所有的子视图都被渲染成同样的透明度，但会在它后面被渲染 |

 

**Core OS  \**** 以下为系统自动修改,无需手动修改****:**

------

 **表A-9 Core OS**

****

| 字段                            | 类型      | 是否必须 | 摘要                                       |
| ----------------------------- | ------- | ---- | ---------------------------------------- |
| LSRequiresIPhoneOS            | Boolean | No   | 这个键时iOS应用运行在设备上面必须的，并且它的值必须时true         |
| CFBundlePackageType           | String  | No   | 用来标识bundle类型的四个字母长的代码( 在iOS中，你至处理应用，但在Mac中，Info.plst还可以引用其他类型的项目) |
| CFBundleInfoDictionaryVersion | String  | Yes  | Info.plist格式的版本信息,     Info.plst的结构很可能会随着时间改变，那么就需要告诉操作系统，当前这个文件对应的版本是什么。 |
| CFBundleExecutable            | String  | Yes  | 该bundle的可执行文件名,     iOS中的应用会被打包成.app文件。在这个文件中包含了所有的资源，并且还有一个可执行文件。这个键时一个字符串，用来指定可执行文件的名称。 |
| CFBundleSignature             | String  | Yes  | 用来标识创建者的四个字母长的代码, 这个键和Mac有关，和iOS没有特别的关系。 |

### CFBundlePackageType

CFBundlePackageType字段指定了bundle的类型，类似于Mac OS 9的文件类型代码。该字段的值包含一个四个字母长的代码。应用程序的代码是‘APPL’；框架的代码是‘FMWK’；可装载bundle的代码是 ‘BND’。如果您需要，您也可以为可装载bundle选择其他特殊的类型代码。   

** CFBundleInfoDictionaryVersion**

CFBundleInfoDictionaryVersion字段指定了属性列表结构的当前版本号。该字段的存在使得可以支持Info.plist格式将来的版本。在您建立一个bundle时，Project Builder会自动产生该字段。

****

**CFBundleExcutable**

 CFBundleExecutable 标识了bundle的可执行主文件的名称。对于一个应用程序来说,就是该应用程序的可执行文件。对于一个可加载bundle,它是一个可以被bundle 动态加载的二进制文件。对于一个框架，它是一个共享库。Project Builder会自动把该字段加入到合适项目的Info.plist文件中。
    对于框架，考虑到启动效率的原因，可执行文件名需要和框架名同名。该可执行文件名不应该包含可用于多种平台的扩展名。

   

注意您必须在bundle的Info.plist文件中包含一个有效的CFBundleExecutable字段。即使当用户重命名应用程序或bundle的目录时，Mac OS X也可以使用这个字段来定位可执行文件和共享库。

**  CFBundleSignature**

****

 CFBundleSignature字段指定了bundle的创建者，类似于Mac OS 9中的文件创建者代码。该字段的值包含四字母长的代码，用来确定每一个bundle。

 

## **本地化:**

------

 **表A-10 本地化**

| 字段                        | 类型     | 是否必须 | 摘要                                       |
| ------------------------- | ------ | ---- | ---------------------------------------- |
| CFBundleLocalizations     | Array  | No   | 系统通过查找你应用提供的Iproj目录来决定你的应用支持哪些语言地区。这个键的值是一个字符串数组，数组中的每一个值都代表支持的地区 |
| CFBundleDevelopmentRegion | String | No   | 当你开发你的应用的时候，你通常会使用你本地的语言来写它。这个键的值是一个字符串，如果用户请求的区域没有必须的资源的话，它用来表示默认的本地化区域 |

 

## **自定义URL和文档类型:**

------

****

**表A-11 自定义URL和文档类型**

****

| 字段                         | 类型    | 是否必须 | 摘要                                       |
| -------------------------- | ----- | ---- | ---------------------------------------- |
| CFBundleURLTypes           | Array | No   | 一组描述了该bundle所支持的URL协议的字典。这个键可以让你指定一个你的应用支持的URL的一个数组 |
| CFBundleDocumentTypes      | Array | No   | 一组描述了该bundle所支持的文档类型的字典。这个键可以让你指定你的应用可以处理哪种类型的文档,这个数组中的值都是一个字典 |
| UIImportedTypeDeclarations | Array | No   | 为了允许你的应用打开那些不属于它的类型，你需要导入那个UTI，并且这个时你要用到的键 |

 CFBundleURLTypes

 CFBundleURLTypes字段包含了一组描述了应用程序所支持的URL协议的字典。它的用途类似于CFBundleDocumentTypes的 作用，但它描述了URL协议而不是文档类型。每一个字典条目对应一个单独的URL协议, 每一个都代表你应用支持的一种URL规则。表A-11-1列出了在每一个字典条目中使用的字段。

****

**表A-11-1 CFBundleURLTypes字典的字段**

****

| 字段                  | 类型     | 描述                                       |
| ------------------- | ------ | ---------------------------------------- |
| CFBundleTypeRole    | String | 该字段定义了那些与URL类型有关的应用程序的角色（即该应用程序与某种文档类型的关系）。它的值可以是Editer，Viewer，Printer，Shell或None。有关这些值的详细描述可以参见“ 文档的配置”。该字段是必须的。( 当打开这个URL时你的应用所扮演的角色) |
| CFBundleURLIconFile | String | 该字段包含了被用于这种URL类型的图标文件名（不包括扩展名）字符串。( 指定对这种URL所使用的图标的文件名) |
| CFBundleURLName     | String | 该字段包含了这种URL类型的抽象名称字符串。为了确保唯一性，建议您使用Java包方式的命名法则。这个名字作为一个字段也会在InfoPlist.strings文件中出现，用来提供该类型名的可读性版本。( 这应该时一个唯一的字符串，用来区分不同的URL类型) |
| CFBundleURLSchemes  | Array  | 该字段包含了一组可被这种类型处理的URL协议。例如：http,ftp等。( 字符串数组，每一个元素代表这个规则支持的URL) |

 

  CFBundleDocumentTypes

 CFBundleDocumentTypes字段保存了一组字典，它包含了该应用程序所支持的文档类型。每一个字典都被称做类型定义字典，并且包含了用于定义文档类型的字段。表A-11-2列出了类型定义字典中支持的字段。

****

**表 A-11-2  CFBundleDocumentTypes字典的字段**

****

| 字段                     | 类型     | 描述                                       |
| ---------------------- | ------ | ---------------------------------------- |
| CFBundleTypeExtensions | Array  | 该字段包含了一组映射到这个类型的文件扩展名。为了打开具有任何扩展名的文档，可以用单个星号“*”。该字段是必须的。 |
| CFBundleTypeIconFile   | String | 图标文件的数组,该字段指定了系统显示该类文档时使用的图标文件名，该图标文件名的扩展名是可选的。如果没有扩展名，系统会根据平台指定一个（例如，Mac OS 9中的.icons）。 |
| CFBundleTypeName       | String | 该字段包含了这种文档类型的抽象名称。通过在适当的InforPlist.strings文件中包含该字段，可以实现对它的本地化。( 唯一的字符串，区分URL类型) |
| CFBundleTypeOSTypes    | Array  | 该字段包含了一组映射到这个类型的四字母长的类型代码。为了打开所有类型的文档，可以把它设为“****”。该字段是必须的。 |
| CFBundleTypeRole       | String | 该字段定义了那些与文档类型有关的应用程序的角色。它的值可以是Editer，Viewer，Printer，Shell或None。有关这些值的详细描述可以参见“ 文档的配置”。该字段是必须的。 |
| NSDocumentClass        | String | 该字段描述了被用来实例化文档的NSDocument子类。仅供Cocoa应用程序使用。 |
| NSExportableAs         | Array  | 该字段描述了一组可以输出的文档类型。仅供Cocoa应用程序使用。         |

 

**使用iCloud:**

------

**表A-12 使用iCloud**

****

| 字段                     | 类型     | 是否必须 | 摘要                                       |
| ---------------------- | ------ | ---- | ---------------------------------------- |
| NSUbiquitousDisplaySet | String | No   | iCloud使用这个键来表示你应用的文件存储。可以把它想象成iCloud中的一个目录用来存放你应用中的文件 |

## **Bundle核心字段:**

------

Mac OS X 为描述bundle的信息提供了一组核心字段。集成开发环境会赋予这些字段缺省值。表A-13列出了这些字段。

****

****

**表A-13 标准字段概要:**

****

| 字段                        | 类型     | 是否必须 | 摘要                                  |
| ------------------------- | ------ | ---- | ----------------------------------- |
| CFBundleDevelopmentRegion | String | No   | 该bundle的地区。通常对应于作者的母语。              |
| CFBundleGetInfoHTML       | String | No   | 用来在Finder的Get Info 面板中显示的更丰富内容的字符串。 |
| CFBundleGetInfoString     | String | No   | 用来在Finder的Get Info 面板中显示的字符串。       |
| CFBundleHelpBookFolder    | String | No   | 含有该bundle帮助文件的文件夹名字。                |
| CFBundleHelpBookName      | String | No   | 当该bundle的帮助启动时显示的帮助文件的名字。           |

****

### CFBundleDevelopmentRegion

CFBundleDevelopmentRegion字段指定了一个字符串值来标识bundle的地区。通常对应于作者的母语。如果不能找到用户首选的地区或语言的资源，系统最后会使用该值。

### CFBundleGetInfoHTML

 CFBundleGetInfoHTML字段含有会在bundle的信息窗口中显示的HTML字符串。如果您希望在信息窗口中有更强的表现力，可以使用这 个键值对来替代纯文本的CFBundleGetInfoString。通过把它加入到合适的.lproj目录中的InfoPlist.strings文件 中，您也可以本地化该字符串。

    如果CFBundleGetInfoString和CFBundleGetInfoHTML同时存在的话，系统会选择使用CFBundleGetInfoHTML。

### CFBundleGetInfoString

CFBundleGetInfoString字段含有会在bundle的信息窗口中显示的纯文本字符串（这里的字符串也就是Mac OS9中的长字符串）。该字段的格式应该遵照Mac OS 9中的长字符串，例如：“2.2.1, ? Great Software, Inc,1999”。通过把它加入到合适的.lproj目录中的InfoPlist.strings文件中，您也可以本地化该字符串。

   

 如果存在CFBundleGetInfoHTML的话，系统不会选择使用该字段。

 

### CFBundleHelpBookFolder

CFBundleHelpBookFolder字段含有该bundle的帮助文件的文件夹名字。帮助通常被本地化成一种指定的语言，所以该字段指向的文件夹应该是所选择语言的.lproj目录中的文件夹。

### CFBundleHelpBookName

CFBundleHelpBookName指定了您的应用程序的帮助主页。该字段指定的帮助页面名可以和HTML文件名不同。在帮助文件META标签的CONTENT属性中指定了帮助页面名。

** **

** **

## **应用程序特定的字段:**

------

****

**表A-14 应用程序特定的字段:**

****

| 字段                       | 类型                | 是否必须 | 摘要                              |
| ------------------------ | ----------------- | ---- | ------------------------------- |
| CFAppleHelpAnchor        | String            | No   | 该bundle的初始HTML帮助文件。             |
| NSAppleScriptEnabled     | String            | No   | 指定是否支持AppleScript。              |
| NSHumanReadableCopyright | String            | Yes  | 显示在对话框中的版权信息。                   |
| NSJavaNeeded             | Boolean or String | No   | 指定该程序是否需要一个Java虚拟机。             |
| NSJavaPath               | Array             | No   | 一组Java类所在的路径（前面需要加上NSJavaRoot）。 |
| NSJavaRoot               | String            | No   | 包含Java类的根目录。                    |
| NSMainNibFile**          | String            | Yes  | 应用程序的主nib文件名。                   |
| NSPrincipalClass         | String            | Yes  | bundle的主类的名字。                   |
| NSServices               | Array             | No   | 一组描述了由应用程序所提供的服务的字典。            |

 

**CFAppleHelpAnchor**

****

 

CFAppleHelpAnchor字段定义了bundle的初始HTML帮助文件名，不需要包括.html或.htm扩展名。这个文件位于bundle的本地化资源目录中，或者如果没有本地化资源目录的话，则直接被放在Resources目录中。

### NSAppleScriptEnabled

NSAppleScriptEnabled字段说明了该应用程序是否支持AppleScript。如果您的应用程序支持，就需要把该字符串的值设为“Yes”。

### NSHumanReadableCopyright

NSHumanReadableCopyright字段包含了一个含有bundle的版权信息的字符串。您可以在“关于”对话框中显示它。该字段通常会出现在InfoPlist.strings文件中，因为往往需要本地化该字段的值。

### NSJavaNeeded

    NSJavaNeeded字段含有一个布尔值，用来确定在执行该bundle的代码之前Java虚拟机是否需要被载入并运行。您也可以指定一个字符串类型的值“YES”代替布尔型的值。

 

### NSJavaPath

 NSJavaPath字段包含了一组路径。每一个路径指向一个Java类。该路径相对于由NSJavaRoot字段定义的位置来说，可能是一个绝对路径也可能是一个相对路径。开发环境会自动把这些值保存在数组中。

### NSJavaRoot

NSJavaRoot字段含有一个指向一个目录的字符串。该目录是应用程序的Java类文件的根目录

### NSPrincipalClass

NSPrincipalClass字段定义了一个bundle的主类的名称。对于应用程序来说，缺省情况下这个名字就是应用程序的名字。

### NSServices

NSServices包含了一组字典，它详细说明了应用程序所提供的服务。表A-5列出了用来指定服务的字段。

****

**表 A-14-1 NSServices字典的字段:**

****

| 字段              | 类型         | 描述                                       |
| --------------- | ---------- | ---------------------------------------- |
| NSPortName      | String     | 该字段指定了由您的应用程序监听器为接受外部服务请求所提供的端口名称。       |
| NSMessage       | String     | 该字段指定了用来调用该服务的实例方法名。在Objective-C中，实例方法的形式是messageName:userData:error:。在Java中，实例方法的形式是messageName(NSPasteBoard.String)。 |
| NSSendTypes     | Array      | 该字段指定了一组可以被该服务读取的数据类型名。NSPasteboard类列出了几个常用的数据类型。您必须包含此字段，NSReturnTypes，或者两者。 |
| NSReturnTypes   | Array      | 该字段指定了一组可以被该服务返回的数据类型名。NSPasteboard类列出了几个常用的数据类型。您必须包含此字段，NSSendTypes，或者两者。 |
| NSMenuItem      | Dictionary | 该 字段包含一个字典，它指定了加入Services菜单中的文本。字典中的唯一一个字段被称为default并且它的值是菜单项的文本。该值必须是唯一的。 您可以使用斜杠“/”来指定一个子菜单。例如，Mail/Send出现在Services菜单中时就是一个带有Send子菜单并且名为Mail的菜单。 |
| NSKeyEquivalent | Dictionary | 该字段是可选的，并且包含一个含有用来请求服务菜单命令的快捷按键的字典。与NSMenuItem类似，字典中的唯一一个字段被称为default并且它的值是单个的字符。用户可以通过按下Command，Shift功能键和相应的字符来请求该快捷按键。 |
| NSUserData      | String     | 该字段是一个可选字符串，它含有您的选择值。                    |
| NSTimeout       | String     | 该字段是一个可选的数字字符串，它指定了从应用程序请求服务到收到它的响应所需要等待的毫秒数。 |

 

**启动服务字段:**

------

****

启动服务字段规定了Mac OS X中的应用程序是怎样被启动的。这些字段适用于CFM和Mach-O可执行文件。有关CFM和Mach-O可执行文件的详情可参见“安装和集成”一章中的“CFM可执行文件”。表A-6列出了启动服务的字段。

****

**表A-15  启动服务字段:**

****

| 字段                | 类型     | 是否必须 | 摘要                                       |
| ----------------- | ------ | ---- | ---------------------------------------- |
| LSBackgroundOnly  | String | No   | 指定了应用程序是否仅仅运行在后台。（仅适用于Mach-O的应用程序）。      |
| LSPrefersCarbon   | String | No   | 指定了应用程序是否优先运行在Carbon环境中。                 |
| LSPrefersClassic  | String | No   | 指定了应用程序是否优先运行在Classic环境中。                |
| LSRequiresCarbon  | String | No   | 指定了应用程序是否必须运行在一个Carbon环境中。               |
| LSRequiresClassic | String | No   | 指定了应用程序是否必须运行在一个Classic环境中。              |
| LSUIElement       | String | No   | 指定了应用程序是否是一个用户界面组件，即一个应用程序不应该出现在Dock中或强制退出窗口。 |

### LSBackgroundOnly

 如果该字段存在并且被设为“1”，启动服务将只会运行在后台。您可以使用该字段来创建无用户界面的后台应用程序。如果您的应用程序使用了连接到窗口服务器 的高级框架，但并不需要显示出来，您也应该使用该字段。后台应用程序必须被编译成Mach-O可执行文件。该选项不适用于CFM应用程序。

   

您也可以指定该字段的类型为Boolean或Number。然而，只有Mac OS X 10.2或以上的版本才支持这些类型的值。

 

### LSPrefersCarbon

如果该字段被设为“1”，Finder将会在显示简介面板中显示“在Classic环境中打开”控制选项，缺省情况下该控件未被选中。如果需要，用户可以修改这个控制选项来在Classic环境中启动应用程序。

   

您也可以指定该字段的类型为Boolean或Number。然而，只有Mac OS X 10.2或以上的版本才支持这些类型的值。如果您在您的属性列表中加入了该字段，那么就不要同时加入LSPrefersClassic, LSRequiresCarbon,或LSRequiresClassic字段。

### LSPrefersClassic

如果该字段被设为“1”，Finder将会在显示简介面板中显示“在Classic环境中打开” 控制选项，缺省情况下该控件被选中。如果需要，用户可以修改这个控制选项来在Carbon环境中启动应用程序。

 您也可以指定该字段的类型为Boolean或Number。然而，只有Mac OS X 10.2或以上的版本才支持这些类型的值。如果您在您的属性列表中加入了该字段，那么就不要同时加入LSPrefersCarbon, LSRequiresCarbon,或LSRequiresClassic字段。

### LSRequiresCarbon

如果该字段被设为“1”，启动服务将只在Carbon环境中运行应用程序。如果您的应用程序不应该运行在Classic环境中的话，可以使用该字段。

    

您也可以指定该字段的类型为Boolean或Number。然而，只有Mac OS X 10.2或以上的版本才支持这些类型的值。如果您在您的属性列表中加入了该字段，那么就不要同时加入LSPrefersCarbon, LSPrefersClassic,或LSRequiresClassic字段。

### LSRequiresClassic

如果该字段被设为“1”，启动服务将只在Classic环境中运行应用程序。如果您的应用程序不应该运行在Carbon兼容环境中的话，可以使用该字段。

   

您也可以指定该字段的类型为Boolean或Number。然而，只有Mac OS X 10.2或以上的版本才支持这些类型的值。如果您在您的属性列表中加入了该字段，那么就不要同时加入LSPrefersCarbon, LSPrefersClassic,或LSRequiresCarbon字段。

### LSUIElement

如果该字段被设为“1”，启动服务会将该应用程序作为一个用户界面组件来运行。用户界面组件不会出现在Dock或强制退出窗口中。虽然它们通常作为后台应 用程序运行，但是如果希望的话，它们也可以在前台显示一个用户界面。点击属于用户界面组件的窗口，应用程序将会处理产生的事件。

   

Dock和登录窗口是两个用户界面组件应用程序。

## **应用程序包字段:**

------

应用程序打包的目的是把一个应用程序打包成一个自我包含的实体，并且对用户隐藏了它的内容。然而，用户常常希望操作应用程序的某些文件。例如，用户可能希 望添加或删除某个插件，本地化资源，等等。开发者可以在Info.plist 文件中指定一些可以由用户维护的项目。那么Finder会把这些项目显示在bundle的信息面板中，并允许用户浏览，删除或添加这些项目。

### CFBundleInstallerInfo

应用程序打包信息的根字段是CFBundleInstallerInfo。该字段定义了一个字典，它包含了表A-7中所列出的字段。“是否必须”列指出了哪些是您必须支持的功能。

**表A-16-1 应用程序打包字段:**

****

| 字段             | 类型     | 是否必须 | 摘要                     |
| -------------- | ------ | ---- | ---------------------- |
| APInstallerURL | String | Yes  | 一个指向您希望安装的文件的URL路径。    |
| APFiles        | Array  | Yes  | 一组字典，描述了那些可以被安装的文件或目录。 |

 

### APInstallerURL

APInstallerURL字段指定了一个指向您希望安装的文件的路径。您必须以file://localhost/path/ 形式来说明这个路径。所有被安装的文件必须位于这个文件夹中。

     

### APFiles

APFiles字段指定了一个字典，描述了您希望安装的文件。每个字典条目可以包含某个文件或目录的描述。您可以让APFiles 字段包含在其自身中，用于指定在目录内部的文件。表A-8列出了用来指定有关单个文件或目录的信息。

****

****

**表A-16-2  APFiles字典字段:**

****

| 字段                     | 类型     | 描述                                       |
| ---------------------- | ------ | ---------------------------------------- |
| APFileDescriptionKey   | String | 用来显示在Finder的信息窗口中的简短描述。                  |
| APDisplayedAsContainer | String | 如果值为“Yes”，该项目作为一个目录图标显示在信息面板中；否则，它被显示为一个文档图标。 |
| APFileDestinationPath  | String | 一个安装组件的相对路径。                             |
| APFileName             | String | 文件或目录的名称。                                |
| APFileSourcePath       | String | 指向应用程序包中组件的路径，相对与APInstallerURL路径。       |
| APInstallAction        | String | 操纵组件的动作：“Copy”或者“Open”                   |

 

 

** UIFileSharingEnabled   应用程序支持itunes共享文件夹   值为 boolean 值   YES 共享；  NO 不共享**

**这个字段在字段编辑器中的名称为： Application supports iTunes file sharing**

整理自:http://www.cnblogs.com/adamleung/p/3494651.html
            http://blog.csdn.net/swj6125/article/details/9791109 

转载请标明出处,谢谢!!!   

如有问题欢迎指正,本人也是参考大神们的文章总结的,可能跟最新的Xcode有点出入!不喜勿喷!

文章上传可能格式上有点问题看着不舒服,欢迎下载该文章,pdf文档下载地址:[https://yunpan.cn/ckRv6yDrKtR5M](https://yunpan.cn/ckRv6yDrKtR5M)（提取码：ce99）



# 注

转载自[http://blog.csdn.net/q375537943/article/details/52666961](http://blog.csdn.net/q375537943/article/details/52666961)