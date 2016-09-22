---
layout: post
title: "PhotoKit的使用"
excerpt: "项目之前选照片用的是AssetsLibrary，为了支持iOS7.0的系统。由于对iCloud的支持不太友好，于是最近决定放弃AssetsLibrary，替换成PhotoKit。之前有了解可以简单地使用，趁这次机会彻底看一下。"
categories: [OC]
tags: [OC, Photos]
date: 2016-06-20
modified: 
comments: true
---

* TOC
{:toc}
---

## 1.从 `Photos/Photos.h`开始看起

```objective-c
//
//  Photos.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#ifndef Photos_Photos_h
#define Photos_Photos_h

#import <Photos/PHPhotoLibrary.h>
#import <Photos/PhotosTypes.h>

#import <Photos/PHObject.h>
#import <Photos/PHAsset.h>
#import <Photos/PHLivePhoto.h>
#import <Photos/PHCollection.h>

#import <Photos/PHFetchOptions.h>
#import <Photos/PHFetchResult.h>

#import <Photos/PHChange.h>

#import <Photos/PHAssetChangeRequest.h>
#import <Photos/PHAssetCreationRequest.h>
#import <Photos/PHAssetCollectionChangeRequest.h>
#import <Photos/PHCollectionListChangeRequest.h>
#import <Photos/PHLivePhotoEditingContext.h>

#import <Photos/PHImageManager.h>

#import <Photos/PHAssetResourceManager.h>
#import <Photos/PHAssetResource.h>

#import <Photos/PHAdjustmentData.h>
#import <Photos/PHContentEditingInput.h>
#import <Photos/PHContentEditingOutput.h>

#import <Photos/PhotosDefines.h>

#endif
```

### Photos/PHPhotoLibrary.h

```objective-c
//
//  PHPhotoLibrary.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Photos/PhotosDefines.h>

NS_ASSUME_NONNULL_BEGIN

@class PHChange;

typedef NS_ENUM(NSInteger, PHAuthorizationStatus) {
    PHAuthorizationStatusNotDetermined = 0, // User has not yet made a choice with regards to this application
    PHAuthorizationStatusRestricted,        // This application is not authorized to access photo data.
                                            // The user cannot change this application’s status, possibly due to active restrictions
                                            //   such as parental controls being in place.
    PHAuthorizationStatusDenied,            // User has explicitly denied this application access to photos data.
    PHAuthorizationStatusAuthorized         // User has authorized this application to access photos data.
} PHOTOS_AVAILABLE_IOS_TVOS(8_0, 10_0);


PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @protocol PHPhotoLibraryChangeObserver <NSObject>
// This callback is invoked on an arbitrary serial queue. If you need this to be handled on a specific queue, you should redispatch appropriately
- (void)photoLibraryDidChange:(PHChange *)changeInstance;

@end

/*!
 @class        PHPhotoLibrary
 @abstract     A PHPhotoLibrary provides access to the metadata and image data for the photos, videos and related content in the user's photo library, including content from the Camera Roll, iCloud Shared, Photo Stream, imported, and synced from iTunes.
 @discussion   ...
 */
PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHPhotoLibrary : NSObject

+ (PHPhotoLibrary *)sharedPhotoLibrary;

+ (PHAuthorizationStatus)authorizationStatus;
+ (void)requestAuthorization:(void(^)(PHAuthorizationStatus status))handler;

#pragma mark - Applying Changes

// handlers are invoked on an arbitrary serial queue
// Nesting change requests will throw an exception
- (void)performChanges:(dispatch_block_t)changeBlock completionHandler:(nullable void(^)(BOOL success, NSError *__nullable error))completionHandler;
- (BOOL)performChangesAndWait:(dispatch_block_t)changeBlock error:(NSError *__autoreleasing *)error;


#pragma mark - Change Handling

- (void)registerChangeObserver:(id<PHPhotoLibraryChangeObserver>)observer;
- (void)unregisterChangeObserver:(id<PHPhotoLibraryChangeObserver>)observer;

@end

NS_ASSUME_NONNULL_END

```

### Photos/PhotosTypes.h

```objective-c
//
//  PhotosTypes.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#ifndef Photos_PhotosTypes_h
#define Photos_PhotosTypes_h

#import <Photos/PhotosDefines.h>

#pragma mark - PHCollectionListTypes

typedef NS_ENUM(NSInteger, PHImageContentMode) {
    PHImageContentModeAspectFit = 0,
    PHImageContentModeAspectFill = 1,
    PHImageContentModeDefault = PHImageContentModeAspectFit
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_ENUM(NSInteger, PHCollectionListType) {
    PHCollectionListTypeMomentList    = 1,
    PHCollectionListTypeFolder        = 2,
    PHCollectionListTypeSmartFolder   = 3,
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_ENUM(NSInteger, PHCollectionListSubtype) {
    
    // PHCollectionListTypeMomentList subtypes
    PHCollectionListSubtypeMomentListCluster    = 1,
    PHCollectionListSubtypeMomentListYear       = 2,
    
    // PHCollectionListTypeFolder subtypes
    PHCollectionListSubtypeRegularFolder        = 100,
    
    // PHCollectionListTypeSmartFolder subtypes
    PHCollectionListSubtypeSmartFolderEvents    = 200,
    PHCollectionListSubtypeSmartFolderFaces     = 201,
    
    // Used for fetching if you don't care about the exact subtype
    PHCollectionListSubtypeAny = NSIntegerMax
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

#pragma mark - PHCollection types

typedef NS_ENUM(NSInteger, PHCollectionEditOperation) {
    PHCollectionEditOperationDeleteContent    = 1, // Delete things it contains
    PHCollectionEditOperationRemoveContent    = 2, // Remove things it contains, they're not deleted from the library
    PHCollectionEditOperationAddContent       = 3, // Add things from other collection
    PHCollectionEditOperationCreateContent    = 4, // Create new things, or duplicate them from others in the same container
    PHCollectionEditOperationRearrangeContent = 5, // Change the order of things
    PHCollectionEditOperationDelete           = 6, // Deleting of the container, not the content
    PHCollectionEditOperationRename           = 7, // Renaming of the container, not the content
} PHOTOS_AVAILABLE_IOS_TVOS(8_0, 10_0);

#pragma mark - PHAssetCollection types

typedef NS_ENUM(NSInteger, PHAssetCollectionType) {
    PHAssetCollectionTypeAlbum      = 1,
    PHAssetCollectionTypeSmartAlbum = 2,
    PHAssetCollectionTypeMoment     = 3,
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_ENUM(NSInteger, PHAssetCollectionSubtype) {
    
    // PHAssetCollectionTypeAlbum regular subtypes
    PHAssetCollectionSubtypeAlbumRegular         = 2,
    PHAssetCollectionSubtypeAlbumSyncedEvent     = 3,
    PHAssetCollectionSubtypeAlbumSyncedFaces     = 4,
    PHAssetCollectionSubtypeAlbumSyncedAlbum     = 5,
    PHAssetCollectionSubtypeAlbumImported        = 6,
    
    // PHAssetCollectionTypeAlbum shared subtypes
    PHAssetCollectionSubtypeAlbumMyPhotoStream   = 100,
    PHAssetCollectionSubtypeAlbumCloudShared     = 101,
    
    // PHAssetCollectionTypeSmartAlbum subtypes
    PHAssetCollectionSubtypeSmartAlbumGeneric    = 200,
    PHAssetCollectionSubtypeSmartAlbumPanoramas  = 201,
    PHAssetCollectionSubtypeSmartAlbumVideos     = 202,
    PHAssetCollectionSubtypeSmartAlbumFavorites  = 203,
    PHAssetCollectionSubtypeSmartAlbumTimelapses = 204,
    PHAssetCollectionSubtypeSmartAlbumAllHidden  = 205,
    PHAssetCollectionSubtypeSmartAlbumRecentlyAdded = 206,
    PHAssetCollectionSubtypeSmartAlbumBursts     = 207,
    PHAssetCollectionSubtypeSmartAlbumSlomoVideos = 208,
    PHAssetCollectionSubtypeSmartAlbumUserLibrary = 209,
    PHAssetCollectionSubtypeSmartAlbumSelfPortraits PHOTOS_AVAILABLE_IOS_TVOS(9_0, 10_0) = 210,
    PHAssetCollectionSubtypeSmartAlbumScreenshots PHOTOS_AVAILABLE_IOS_TVOS(9_0, 10_0) = 211,
    
    // Used for fetching, if you don't care about the exact subtype
    PHAssetCollectionSubtypeAny = NSIntegerMax
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

#pragma mark - PHAsset types

typedef NS_ENUM(NSInteger, PHAssetEditOperation) {
    PHAssetEditOperationDelete     = 1,
    PHAssetEditOperationContent    = 2,
    PHAssetEditOperationProperties = 3,
} PHOTOS_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_ENUM(NSInteger, PHAssetMediaType) {
    PHAssetMediaTypeUnknown = 0,
    PHAssetMediaTypeImage   = 1,
    PHAssetMediaTypeVideo   = 2,
    PHAssetMediaTypeAudio   = 3,
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_OPTIONS(NSUInteger, PHAssetMediaSubtype) {
    PHAssetMediaSubtypeNone               = 0,
    
    // Photo subtypes
    PHAssetMediaSubtypePhotoPanorama      = (1UL << 0),
    PHAssetMediaSubtypePhotoHDR           = (1UL << 1),
    PHAssetMediaSubtypePhotoScreenshot PHOTOS_AVAILABLE_IOS_TVOS(9_0, 10_0) = (1UL << 2),
    PHAssetMediaSubtypePhotoLive PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0) = (1UL << 3),

    // Video subtypes
    PHAssetMediaSubtypeVideoStreamed      = (1UL << 16),
    PHAssetMediaSubtypeVideoHighFrameRate = (1UL << 17),
    PHAssetMediaSubtypeVideoTimelapse     = (1UL << 18),
} PHOTOS_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_OPTIONS(NSUInteger, PHAssetBurstSelectionType) {
    PHAssetBurstSelectionTypeNone     = 0,
    PHAssetBurstSelectionTypeAutoPick = (1UL << 0),
    PHAssetBurstSelectionTypeUserPick = (1UL << 1),
} PHOTOS_AVAILABLE_IOS_TVOS(8_0, 10_0);

typedef NS_OPTIONS(NSUInteger, PHAssetSourceType) {
    PHAssetSourceTypeNone            = 0,
    PHAssetSourceTypeUserLibrary     = (1UL << 0),
    PHAssetSourceTypeCloudShared     = (1UL << 1),
    PHAssetSourceTypeiTunesSynced    = (1UL << 2),
} PHOTOS_AVAILABLE_IOS_TVOS(9_0, 10_0);

typedef NS_ENUM(NSInteger, PHAssetResourceType) {
    PHAssetResourceTypePhoto                             = 1,
    PHAssetResourceTypeVideo                             = 2,
    PHAssetResourceTypeAudio                             = 3,
    PHAssetResourceTypeAlternatePhoto                    = 4,
    PHAssetResourceTypeFullSizePhoto                     = 5,
    PHAssetResourceTypeFullSizeVideo                     = 6,
    PHAssetResourceTypeAdjustmentData                    = 7,
    PHAssetResourceTypeAdjustmentBasePhoto               = 8,
    PHAssetResourceTypePairedVideo PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0) = 9,
    PHAssetResourceTypeFullSizePairedVideo PHOTOS_AVAILABLE_IOS_TVOS(10_0, 10_0) = 10,
    PHAssetResourceTypeAdjustmentBasePairedVideo PHOTOS_AVAILABLE_IOS_TVOS(10_0, 10_0) = 11,
} PHOTOS_ENUM_AVAILABLE_IOS_TVOS(9_0, 10_0);

#endif

```

### Photos/PHObject.h

```objective-c
//
//  PHObject.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Photos/PhotosDefines.h>

NS_ASSUME_NONNULL_BEGIN

@class PHPhotoLibrary;


PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHObject : NSObject <NSCopying>

// Returns an identifier which persistently identifies the object on a given device
@property (nonatomic, copy, readonly) NSString *localIdentifier;

@end

// PHObjectPlaceholder represents a model object future , vended by change requests when creating a model object.  PHObjectPlaceholder is a read-only object and may be used as a proxy for the real object that will be created both inside and outside of the change block.  Will compare isEqual: to the fetched model object after the change block is performed.
PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHObjectPlaceholder : PHObject
@end

NS_ASSUME_NONNULL_END

```

### Photos/PHAsset.h

```objective-c
//
//  PHAsset.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#import <Photos/PHObject.h>
#import <Photos/PhotosTypes.h>
#import <Photos/PHFetchResult.h>
#import <Photos/PHPhotoLibrary.h>
#import <Photos/PhotosDefines.h>

#import <UIKit/UIImage.h>
#import <ImageIO/ImageIO.h>
#import <CoreLocation/CLLocation.h>


@class PHFetchOptions;
@class PHAssetCollection;
@class PHPerson;
@class PHFaceCollection;

NS_ASSUME_NONNULL_BEGIN

PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHAsset : PHObject

#pragma mark - Properties

@property (nonatomic, assign, readonly) PHAssetMediaType mediaType;
@property (nonatomic, assign, readonly) PHAssetMediaSubtype mediaSubtypes;

@property (nonatomic, assign, readonly) NSUInteger pixelWidth;
@property (nonatomic, assign, readonly) NSUInteger pixelHeight;

@property (nonatomic, strong, readonly, nullable) NSDate *creationDate;
@property (nonatomic, strong, readonly, nullable) NSDate *modificationDate;

@property (nonatomic, strong, readonly, nullable) CLLocation *location;

@property (nonatomic, assign, readonly) NSTimeInterval duration;

// a hidden asset will be excluded from moment collections, but may still be included in other smart or regular album collections
@property (nonatomic, assign, readonly, getter=isHidden) BOOL hidden;

@property (nonatomic, assign, readonly, getter=isFavorite) BOOL favorite;

@property (nonatomic, strong, readonly, nullable) NSString *burstIdentifier;
@property (nonatomic, assign, readonly) PHAssetBurstSelectionType burstSelectionTypes;
@property (nonatomic, assign, readonly) BOOL representsBurst;

@property (nonatomic, assign, readonly) PHAssetSourceType sourceType PHOTOS_AVAILABLE_IOS_TVOS(9_0, 10_0);

#pragma mark - Capabilities

- (BOOL)canPerformEditOperation:(PHAssetEditOperation)editOperation;

#pragma mark - Fetching assets

+ (PHFetchResult<PHAsset *> *)fetchAssetsInAssetCollection:(PHAssetCollection *)assetCollection options:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHAsset *> *)fetchAssetsWithLocalIdentifiers:(NSArray<NSString *> *)identifiers options:(nullable PHFetchOptions *)options;
+ (nullable PHFetchResult<PHAsset *> *)fetchKeyAssetsInAssetCollection:(PHAssetCollection *)assetCollection options:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHAsset *> *)fetchAssetsWithBurstIdentifier:(NSString *)burstIdentifier options:(nullable PHFetchOptions *)options;

// Fetches PHAssetSourceTypeUserLibrary assets by default (use includeAssetSourceTypes option to override)
+ (PHFetchResult<PHAsset *> *)fetchAssetsWithOptions:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHAsset *> *)fetchAssetsWithMediaType:(PHAssetMediaType)mediaType options:(nullable PHFetchOptions *)options;

// assetURLs are URLs retrieved from ALAsset's ALAssetPropertyAssetURL
+ (PHFetchResult<PHAsset *> *)fetchAssetsWithALAssetURLs:(NSArray<NSURL *> *)assetURLs options:(nullable PHFetchOptions *)options;

@end

NS_ASSUME_NONNULL_END

```

### Photos/PHLivePhoto.h

```objective-c
//
//  PHLivePhoto.h
//  PhotoKit
//
//  Copyright © 2015 Apple Inc. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

#import <Photos/PhotosDefines.h>

#import "PhotosTypes.h"

NS_ASSUME_NONNULL_BEGIN

typedef int32_t PHLivePhotoRequestID PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0);
static const PHLivePhotoRequestID PHLivePhotoRequestIDInvalid = 0;

/// These keys may be found in the info dictionary delivered to a live photo request result handler block.
extern NSString * const PHLivePhotoInfoErrorKey PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0); // key : NSError decribing an error that has occurred while creating the live photo
extern NSString * const PHLivePhotoInfoIsDegradedKey PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0); // key : NSNumber containing a BOOL, YES whenever the deivered live photo object does not contain all content required for full playback.
extern NSString * const PHLivePhotoInfoCancelledKey PHOTOS_AVAILABLE_IOS_TVOS(9_1, 10_0); // key : NSNumber containing a BOOL, YES when the result handler is being called after the request has been cancelled.


PHOTOS_CLASS_AVAILABLE_IOS_TVOS(9_1, 10_0)
@interface PHLivePhoto : NSObject <NSCopying, NSSecureCoding>

/// The dimensions of the live photo measured in pixels.
@property (readonly, nonatomic) CGSize size;

#pragma mark - Export

/// Requests a Live Photo from the given resource URLs. The result handler will be called multiple times to deliver new PHLivePhoto instances with increasingly more content. If a placeholder image is provided, the result handler will first be invoked synchronously to deliver a live photo containing only the placeholder image. Subsequent invocations of the result handler will occur on the main queue.
//  The targetSize and contentMode parameters are used to resize the live photo content if needed. If targetSize is equal to CGRectZero, content will not be resized.
//  When using this method to provide content for a PHLivePhotoView, each live photo instance delivered via the result handler should be passed to -[PHLivePhotoView setLivePhoto:].
+ (PHLivePhotoRequestID)requestLivePhotoWithResourceFileURLs:(NSArray<NSURL *> *)fileURLs placeholderImage:(UIImage *__nullable)image targetSize:(CGSize)targetSize contentMode:(PHImageContentMode)contentMode resultHandler:(void(^)(PHLivePhoto *__nullable livePhoto, NSDictionary *info))resultHandler;

/// Cancels the loading of a PHLivePhoto. The request's completion handler will be called.
+ (void)cancelLivePhotoRequestWithRequestID:(PHLivePhotoRequestID)requestID;

@end


NS_ASSUME_NONNULL_END

```

### Photos/PHCollection.h

```objective-c
//
//  PHCollection.h
//  Photos
//
//  Copyright (c) 2013 Apple Inc. All rights reserved.
//

#import <Photos/PHObject.h>
#import <Photos/PHFetchResult.h>
#import <Photos/PhotosTypes.h>
#import <Photos/PhotosDefines.h>

@class PHAsset, PHCollectionList, PHFetchResult, PHFetchOptions;
@class CLLocation;

NS_ASSUME_NONNULL_BEGIN

PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHCollection : PHObject

@property (nonatomic, assign, readonly) BOOL canContainAssets;
@property (nonatomic, assign, readonly) BOOL canContainCollections;
@property (nonatomic, strong, readonly, nullable) NSString *localizedTitle;

#pragma mark - Capabilities

- (BOOL)canPerformEditOperation:(PHCollectionEditOperation)anOperation;


#pragma mark - Fetching collections

+ (PHFetchResult<PHCollection *> *)fetchCollectionsInCollectionList:(PHCollectionList *)collectionList options:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHCollection *> *)fetchTopLevelUserCollectionsWithOptions:(nullable PHFetchOptions *)options;

@end


PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHAssetCollection : PHCollection

@property (nonatomic, assign, readonly) PHAssetCollectionType assetCollectionType;
@property (nonatomic, assign, readonly) PHAssetCollectionSubtype assetCollectionSubtype;

// These counts are just estimates; the actual count of objects returned from a fetch should be used if you care about accuracy. Returns NSNotFound if a count cannot be quickly returned.
@property (nonatomic, assign, readonly) NSUInteger estimatedAssetCount;

@property (nonatomic, strong, readonly, nullable) NSDate *startDate;
@property (nonatomic, strong, readonly, nullable) NSDate *endDate;

@property (nonatomic, strong, readonly, nullable) CLLocation *approximateLocation;
@property (nonatomic, strong, readonly) NSArray<NSString *> *localizedLocationNames;


#pragma mark - Fetching asset collections

// Fetch asset collections of a single type matching the provided local identifiers (type is inferred from the local identifiers)
+ (PHFetchResult<PHAssetCollection *> *)fetchAssetCollectionsWithLocalIdentifiers:(NSArray<NSString *> *)identifiers options:(nullable PHFetchOptions *)options;

// Fetch asset collections of a single type and subtype provided (use PHAssetCollectionSubtypeAny to match all subtypes)
+ (PHFetchResult<PHAssetCollection *> *)fetchAssetCollectionsWithType:(PHAssetCollectionType)type subtype:(PHAssetCollectionSubtype)subtype options:(nullable PHFetchOptions *)options;

// Smart Albums are not supported, only Albums and Moments
+ (PHFetchResult<PHAssetCollection *> *)fetchAssetCollectionsContainingAsset:(PHAsset *)asset withType:(PHAssetCollectionType)type options:(nullable PHFetchOptions *)options;

// assetGroupURLs are URLs retrieved from ALAssetGroup's ALAssetsGroupPropertyURL
+ (PHFetchResult<PHAssetCollection *> *)fetchAssetCollectionsWithALAssetGroupURLs:(NSArray<NSURL *> *)assetGroupURLs options:(nullable PHFetchOptions *)options;


#pragma mark - Fetching moment asset collections

+ (PHFetchResult<PHAssetCollection *> *)fetchMomentsInMomentList:(PHCollectionList *)momentList options:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHAssetCollection *> *)fetchMomentsWithOptions:(nullable PHFetchOptions *)options;


#pragma mark - Transient asset collections
// These asset collections are only in-memory and are not persisted to disk

+ (PHAssetCollection *)transientAssetCollectionWithAssets:(NSArray<PHAsset *> *)assets title:(nullable NSString *)title;
+ (PHAssetCollection *)transientAssetCollectionWithAssetFetchResult:(PHFetchResult<PHAsset *> *)fetchResult title:(nullable NSString *)title;


@end


PHOTOS_CLASS_AVAILABLE_IOS_TVOS(8_0, 10_0) @interface PHCollectionList : PHCollection

@property (nonatomic, assign, readonly) PHCollectionListType collectionListType;
@property (nonatomic, assign, readonly) PHCollectionListSubtype collectionListSubtype;

@property (nonatomic, strong, readonly, nullable) NSDate *startDate;
@property (nonatomic, strong, readonly, nullable) NSDate *endDate;

@property (nonatomic, strong, readonly) NSArray<NSString *> *localizedLocationNames;


#pragma mark - Fetching collection lists

// A PHAssetCollectionTypeMoment will be contained by a PHCollectionListSubtypeMomentListCluster and a PHCollectionListSubtypeMomentListYear
// Non-moment PHAssetCollections will only be contained by a single collection list
+ (PHFetchResult<PHCollectionList *> *)fetchCollectionListsContainingCollection:(PHCollection *)collection options:(nullable PHFetchOptions *)options;

// Fetch collection lists of a single type matching the provided local identifiers (type is inferred from the local identifiers)
+ (PHFetchResult<PHCollectionList *> *)fetchCollectionListsWithLocalIdentifiers:(NSArray<NSString *> *)identifiers options:(nullable PHFetchOptions *)options;

// Fetch asset collections of a single type and subtype provided (use PHCollectionListSubtypeAny to match all subtypes)
+ (PHFetchResult<PHCollectionList *> *)fetchCollectionListsWithType:(PHCollectionListType)collectionListType subtype:(PHCollectionListSubtype)subtype options:(nullable PHFetchOptions *)options;


#pragma mark - Fetching moment collection lists

+ (PHFetchResult<PHCollectionList *> *)fetchMomentListsWithSubtype:(PHCollectionListSubtype)momentListSubtype containingMoment:(PHAssetCollection *)moment options:(nullable PHFetchOptions *)options;
+ (PHFetchResult<PHCollectionList *> *)fetchMomentListsWithSubtype:(PHCollectionListSubtype)momentListSubtype options:(nullable PHFetchOptions *)options;


#pragma mark - Transient collection lists

// These collection lists are only in-memory and are not persisted to disk
+ (PHCollectionList *)transientCollectionListWithCollections:(NSArray<PHCollection *> *)collections title:(nullable NSString *)title;
+ (PHCollectionList *)transientCollectionListWithCollectionsFetchResult:(PHFetchResult<PHCollection *> *)fetchResult title:(nullable NSString *)title;

@end

NS_ASSUME_NONNULL_END

```

### 