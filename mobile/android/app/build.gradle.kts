plugins {
    id("com.android.application")
    id("com.chaquo.python")
}

fun quoted(value: String): String = "\"" + value
    .replace("\\", "\\\\")
    .replace("\"", "\\\"") + "\""

val revenueCatApiKey = providers.gradleProperty("REVENUECAT_API_KEY")
    .orElse(providers.environmentVariable("REVENUECAT_API_KEY"))
    .getOrElse("")
val revenueCatEntitlement = providers.gradleProperty("REVENUECAT_ENTITLEMENT_ID")
    .orElse(providers.environmentVariable("REVENUECAT_ENTITLEMENT_ID"))
    .getOrElse("sacred_table")

android {
    namespace = "org.theinterdependency.tiwcg"
    compileSdk = 36

    defaultConfig {
        applicationId = "org.theinterdependency.tiwcg"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"

        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }

        buildConfigField("String", "REVENUECAT_API_KEY", quoted(revenueCatApiKey))
        buildConfigField("String", "REVENUECAT_ENTITLEMENT_ID", quoted(revenueCatEntitlement))
    }

    buildFeatures {
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

chaquopy {
    defaultConfig {
        version = "3.12"
    }
    sourceSets {
        getByName("main") {
            srcDir("src/main/python")
            srcDir("../../../engine")
            srcDir("../../../render")
        }
    }
}

dependencies {
    implementation("com.revenuecat.purchases:purchases:10.15.1")
}
