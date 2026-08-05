#!/bin/bash
# Create Xcode project for StreamFusion

echo "Creating Xcode project for StreamFusion..."

PROJECT_DIR="StreamFusion.xcodeproj"
mkdir -p "$PROJECT_DIR"

# Create project.pbxproj
cat > "$PROJECT_DIR/project.pbxproj" << 'EOF'
// !$*UTF8*$!
{
    archiveVersion = 1;
    classes = {
    };
    objectVersion = 56;
    objects = {
        /* Begin PBXBuildFile section */
        000000000000000000000001 /* main.swift in Sources */ = {isa = PBXBuildFile; fileRef = 000000000000000000000002 /* main.swift */; };
        /* End PBXBuildFile section */

        /* Begin PBXFileReference section */
        000000000000000000000000 /* StreamFusion.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = StreamFusion.app; sourceTree = BUILT_PRODUCTS_DIR; };
        000000000000000000000002 /* main.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = main.swift; sourceTree = "<group>"; };
        000000000000000000000003 /* Info.plist */ = {isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; };
        /* End PBXFileReference section */

        /* Begin PBXFrameworksBuildPhase section */
        000000000000000000000004 /* Frameworks */ = {
            isa = PBXFrameworksBuildPhase;
            buildActionMask = 2147483647;
            files = (
            );
            runOnlyForDeploymentPostprocessing = 0;
        };
        /* End PBXFrameworksBuildPhase section */

        /* Begin PBXGroup section */
        000000000000000000000005 = {
            isa = PBXGroup;
            children = (
                000000000000000000000006 /* StreamFusion */,
                000000000000000000000007 /* Products */,
            );
            sourceTree = "<group>";
        };
        000000000000000000000006 /* StreamFusion */ = {
            isa = PBXGroup;
            children = (
                000000000000000000000002 /* main.swift */,
                000000000000000000000003 /* Info.plist */,
            );
            path = StreamFusion;
            sourceTree = "<group>";
        };
        000000000000000000000007 /* Products */ = {
            isa = PBXGroup;
            children = (
                000000000000000000000000 /* StreamFusion.app */,
            );
            name = Products;
            sourceTree = "<group>";
        };
        /* End PBXGroup section */

        /* Begin PBXNativeTarget section */
        000000000000000000000008 /* StreamFusion */ = {
            isa = PBXNativeTarget;
            buildConfigurationList = 000000000000000000000009 /* Build configuration list for PBXNativeTarget "StreamFusion" */;
            buildPhases = (
                00000000000000000000000A /* Sources */,
                000000000000000000000004 /* Frameworks */,
                00000000000000000000000B /* Resources */,
            );
            buildRules = (
            );
            dependencies = (
            );
            name = StreamFusion;
            productName = StreamFusion;
            productReference = 000000000000000000000000 /* StreamFusion.app */;
            productType = "com.apple.product-type.application";
        };
        /* End PBXNativeTarget section */

        /* Begin PBXProject section */
        00000000000000000000000C /* Project object */ = {
            isa = PBXProject;
            buildConfigurationList = 00000000000000000000000D /* Build configuration list for PBXProject "StreamFusion" */;
            compatibilityVersion = "Xcode 14.0";
            developmentRegion = en;
            hasScannedForEncodings = 0;
            knownRegions = (
                en,
                Base,
            );
            mainGroup = 000000000000000000000005;
            productRefGroup = 000000000000000000000007 /* Products */;
            projectDirPath = "";
            projectRoot = "";
            targets = (
                000000000000000000000008 /* StreamFusion */,
            );
        };
        /* End PBXProject section */

        /* Begin PBXResourcesBuildPhase section */
        00000000000000000000000B /* Resources */ = {
            isa = PBXResourcesBuildPhase;
            buildActionMask = 2147483647;
            files = (
            );
            runOnlyForDeploymentPostprocessing = 0;
        };
        /* End PBXResourcesBuildPhase section */

        /* Begin PBXSourcesBuildPhase section */
        00000000000000000000000A /* Sources */ = {
            isa = PBXSourcesBuildPhase;
            buildActionMask = 2147483647;
            files = (
                000000000000000000000001 /* main.swift in Sources */,
            );
            runOnlyForDeploymentPostprocessing = 0;
        };
        /* End PBXSourcesBuildPhase section */

        /* Begin XCBuildConfiguration section */
        00000000000000000000000E /* Debug */ = {
            isa = XCBuildConfiguration;
            buildSettings = {
                ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
                CODE_SIGN_STYLE = Automatic;
                COMBINE_HIDPI_IMAGES = YES;
                CURRENT_PROJECT_VERSION = 1;
                INFOPLIST_FILE = StreamFusion/Info.plist;
                LD_RUNPATH_SEARCH_PATHS = (
                    "$(inherited)",
                    "@executable_path/../Frameworks",
                );
                MACOSX_DEPLOYMENT_TARGET = 11.0;
                MARKETING_VERSION = 1.0;
                PRODUCT_BUNDLE_IDENTIFIER = com.nullframe.streamfusion;
                PRODUCT_NAME = "$(TARGET_NAME)";
                SWIFT_EMIT_LOC_STRINGS = YES;
                SWIFT_VERSION = 5.0;
            };
            name = Debug;
        };
        00000000000000000000000F /* Release */ = {
            isa = XCBuildConfiguration;
            buildSettings = {
                ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
                CODE_SIGN_STYLE = Automatic;
                COMBINE_HIDPI_IMAGES = YES;
                CURRENT_PROJECT_VERSION = 1;
                INFOPLIST_FILE = StreamFusion/Info.plist;
                LD_RUNPATH_SEARCH_PATHS = (
                    "$(inherited)",
                    "@executable_path/../Frameworks",
                );
                MACOSX_DEPLOYMENT_TARGET = 11.0;
                MARKETING_VERSION = 1.0;
                PRODUCT_BUNDLE_IDENTIFIER = com.nullframe.streamfusion;
                PRODUCT_NAME = "$(TARGET_NAME)";
                SWIFT_EMIT_LOC_STRINGS = YES;
                SWIFT_VERSION = 5.0;
            };
            name = Release;
        };
        000000000000000000000010 /* Debug */ = {
            isa = XCBuildConfiguration;
            buildSettings = {
                ALWAYS_SEARCH_USER_PATHS = NO;
                CLANG_ANALYZER_NONNULL = YES;
                CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
                CLANG_CXX_LANGUAGE_STANDARD = "gnu++17";
                CLANG_ENABLE_MODULES = YES;
                CLANG_ENABLE_OBJC_ARC = YES;
                CLANG_ENABLE_OBJC_WEAK = YES;
                CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
                CLANG_WARN_BOOL_CONVERSION = YES;
                CLANG_WARN_COMMA = YES;
                CLANG_WARN_CONSTANT_CONVERSION = YES;
                CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
                CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
                CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
                CLANG_WARN_EMPTY_BODY = YES;
                CLANG_WARN_ENUM_CONVERSION = YES;
                CLANG_WARN_INFINITE_RECURSION = YES;
                CLANG_WARN_INT_CONVERSION = YES;
                CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
                CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
                CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
                CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
                CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
                CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
                CLANG_WARN_STRICT_PROTOTYPES = YES;
                CLANG_WARN_SUSPICIOUS_MOVE = YES;
                CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
                CLANG_WARN_UNREACHABLE_CODE = YES;
                CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
                COPY_PHASE_STRIP = NO;
                DEBUG_INFORMATION_FORMAT = dwarf;
                ENABLE_STRICT_OBJC_MSGSEND = YES;
                ENABLE_TESTABILITY = YES;
                GCC_C_LANGUAGE_STANDARD = gnu11;
                GCC_DYNAMIC_NO_PIC = NO;
                GCC_NO_COMMON_BLOCKS = YES;
                GCC_OPTIMIZATION_LEVEL = 0;
                GCC_PREPROCESSOR_DEFINITIONS = (
                    "DEBUG=1",
                    "$(inherited)",
                );
                GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
                GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
                GCC_WARN_UNDECLARED_SELECTOR = YES;
                GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
                GCC_WARN_UNUSED_FUNCTION = YES;
                GCC_WARN_UNUSED_VARIABLE = YES;
                MACOSX_DEPLOYMENT_TARGET = 11.0;
                MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
                MTL_FAST_MATH = YES;
                ONLY_ACTIVE_ARCH = YES;
                SDKROOT = macosx;
                SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
                SWIFT_OPTIMIZATION_LEVEL = "-Onone";
            };
            name = Debug;
        };
        000000000000000000000011 /* Release */ = {
            isa = XCBuildConfiguration;
            buildSettings = {
                ALWAYS_SEARCH_USER_PATHS = NO;
                CLANG_ANALYZER_NONNULL = YES;
                CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
                CLANG_CXX_LANGUAGE_STANDARD = "gnu++17";
                CLANG_ENABLE_MODULES = YES;
                CLANG_ENABLE_OBJC_ARC = YES;
                CLANG_ENABLE_OBJC_WEAK = YES;
                CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
                CLANG_WARN_BOOL_CONVERSION = YES;
                CLANG_WARN_COMMA = YES;
                CLANG_WARN_CONSTANT_CONVERSION = YES;
                CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
                CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
                CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
                CLANG_WARN_EMPTY_BODY = YES;
                CLANG_WARN_ENUM_CONVERSION = YES;
                CLANG_WARN_INFINITE_RECURSION = YES;
                CLANG_WARN_INT_CONVERSION = YES;
                CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
                CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
                CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
                CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
                CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
                CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
                CLANG_WARN_STRICT_PROTOTYPES = YES;
                CLANG_WARN_SUSPICIOUS_MOVE = YES;
                CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
                CLANG_WARN_UNREACHABLE_CODE = YES;
                CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
                COPY_PHASE_STRIP = NO;
                DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
                ENABLE_NS_ASSERTIONS = NO;
                ENABLE_STRICT_OBJC_MSGSEND = YES;
                GCC_C_LANGUAGE_STANDARD = gnu11;
                GCC_NO_COMMON_BLOCKS = YES;
                GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
                GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
                GCC_WARN_UNDECLARED_SELECTOR = YES;
                GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
                GCC_WARN_UNUSED_FUNCTION = YES;
                GCC_WARN_UNUSED_VARIABLE = YES;
                MACOSX_DEPLOYMENT_TARGET = 11.0;
                MTL_ENABLE_DEBUG_INFO = NO;
                MTL_FAST_MATH = YES;
                SDKROOT = macosx;
                SWIFT_COMPILATION_MODE = wholemodule;
                SWIFT_OPTIMIZATION_LEVEL = "-O";
            };
            name = Release;
        };
        /* End XCBuildConfiguration section */

        /* Begin XCConfigurationList section */
        00000000000000000000000D /* Build configuration list for PBXProject "StreamFusion" */ = {
            isa = XCConfigurationList;
            buildConfigurations = (
                000000000000000000000010 /* Debug */,
                000000000000000000000011 /* Release */,
            );
            defaultConfigurationIsVisible = 0;
            defaultConfigurationName = Release;
        };
        000000000000000000000009 /* Build configuration list for PBXNativeTarget "StreamFusion" */ = {
            isa = XCConfigurationList;
            buildConfigurations = (
                00000000000000000000000E /* Debug */,
                00000000000000000000000F /* Release */,
            );
            defaultConfigurationIsVisible = 0;
            defaultConfigurationName = Release;
        };
        /* End XCConfigurationList section */
    };
    rootObject = 00000000000000000000000C /* Project object */;
}
EOF

echo "✓ Xcode project created: $PROJECT_DIR"
echo ""
echo "To build:"
echo "  open $PROJECT_DIR"
echo ""
echo "Or use xcodebuild:"
echo "  xcodebuild -project $PROJECT_DIR -scheme StreamFusion build"
