## 🔍 Runtime Security

### 1. Root Detection

```kotlin
// RootDetector.kt
object RootDetector {
    
    private val knownRootApps = listOf(
        "com.noshufou.android.su",
        "com.noshufou.android.su.elite",
        "eu.chainfire.supersu",
        "com.koushikdutta.superuser",
        "com.thirdparty.superuser",
        "com.yellowes.su",
        "com.topjohnwu.magisk",
        "com.kingroot.kinguser",
        "com.kingo.root",
        "com.smedialink.oneclickroot",
        "com.zhiqupk.root.global",
        "com.alephzain.framaroot"
    )
    
    private val knownDangerousApps = listOf(
        "com.koushikdutta.rommanager",
        "com.koushikdutta.rommanager.license",
        "com.dimonvideo.luckypatcher",
        "com.chelpus.lackypatch",
        "com.ramdroid.appquarantine",
        "com.ramdroid.appquarantinepro",
        "com.android.vending.billing.InAppBillingService.COIN",
        "com.android.vending.billing.InAppBillingService.LUCK",
        "com.chelpus.luckypatcher",
        "com.blackmartalpha",
        "org.blackmart.market",
        "com.allinone.free",
        "com.repodroid.app",
        "org.creeplays.hack",
        "com.baseappfull.fwd",
        "com.zmapp",
        "com.dv.marketmod.installer",
        "org.mobilism.android",
        "com.android.wp.net.log",
        "com.android.camera.update",
        "cc.madkite.freedom",
        "com.solohsu.android.edxp.manager",
        "org.meowcat.edxposed.manager",
        "com.xmodgame",
        "com.cih.game_cih",
        "com.charles.lpoqasert",
        "catch_.me_.if_.you_.can_"
    )
    
    private val knownRootCloakingPackages = listOf(
        "com.devadvance.rootcloak",
        "com.devadvance.rootcloakplus",
        "de.robv.android.xposed.installer",
        "com.saurik.substrate",
        "com.zachspong.temprootremovejb",
        "com.amphoras.hidemyroot",
        "com.amphoras.hidemyrootadfree",
        "com.formyhm.hiderootPremium",
        "com.formyhm.hideroot"
    )
    
    private val suBinaryPaths = arrayOf(
        "/data/local/",
        "/data/local/bin/",
        "/data/local/xbin/",
        "/sbin/",
        "/su/bin/",
        "/system/bin/",
        "/system/bin/.ext/",
        "/system/bin/failsafe/",
        "/system/sd/xbin/",
        "/system/usr/we-need-root/",
        "/system/xbin/",
        "/cache/",
        "/data/",
        "/dev/"
    )
    
    fun isRooted(): Boolean {
        return checkRootMethod1() || 
               checkRootMethod2() || 
               checkRootMethod3() ||
               checkForRootApps() ||
               checkForDangerousApps() ||
               checkForRootCloakingApps() ||
               checkSuExists() ||
               checkForBusyBoxBinary() ||
               checkForRWPaths()
    }
    
    // Method 1: Check Build tags
    private fun checkRootMethod1(): Boolean {
        val buildTags = Build.TAGS
        return buildTags != null && buildTags.contains("test-keys")
    }
    
    // Method 2: Check for SU binary
    private fun checkRootMethod2(): Boolean {
        return try {
            File("/system/app/Superuser.apk").exists()
        } catch (e: Exception) {
            false
        }
    }
    
    // Method 3: Try to execute SU command
    private fun checkRootMethod3(): Boolean {
        var process: Process? = null
        return try {
            process = Runtime.getRuntime().exec(arrayOf("/system/xbin/which", "su"))
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            bufferedReader.readLine() != null
        } catch (e: Exception) {
            false
        } finally {
            process?.destroy()
        }
    }
    
    private fun checkForRootApps(): Boolean {
        return knownRootApps.any { isPackageInstalled(it) }
    }
    
    private fun checkForDangerousApps(): Boolean {
        return knownDangerousApps.any { isPackageInstalled(it) }
    }
    
    private fun checkForRootCloakingApps(): Boolean {
        return knownRootCloakingPackages.any { isPackageInstalled(it) }
    }
    
    private fun isPackageInstalled(packageName: String): Boolean {
        return try {
            val packageManager = context.packageManager
            packageManager.getPackageInfo(packageName, 0)
            true
        } catch (e: PackageManager.NameNotFoundException) {
            false
        }
    }
    
    private fun checkSuExists(): Boolean {
        return suBinaryPaths.any { path ->
            val file = File(path, "su")
            file.exists()
        }
    }
    
    private fun checkForBusyBoxBinary(): Boolean {
        return try {
            val process = Runtime.getRuntime().exec(arrayOf("which", "busybox"))
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            bufferedReader.readLine() != null
        } catch (e: Exception) {
            false
        }
    }
    
    private fun checkForRWPaths(): Boolean {
        val paths = arrayOf(
            "/system",
            "/system/bin",
            "/system/sbin",
            "/system/xbin",
            "/vendor/bin",
            "/sbin",
            "/etc"
        )
        
        return paths.any { path ->
            try {
                val file = File(path)
                file.canWrite()
            } catch (e: Exception) {
                false
            }
        }
    }
    
    private lateinit var context: Context
    
    fun initialize(context: Context) {
        this.context = context.applicationContext
    }
}
```

### 2. Emulator Detection

```kotlin
// EmulatorDetector.kt
object EmulatorDetector {
    
    fun isEmulator(): Boolean {
        return checkBasic() ||
               checkAdvanced() ||
               checkFiles() ||
               checkQEmuDrivers() ||
               checkIpAddresses()
    }
    
    private fun checkBasic(): Boolean {
        return (Build.FINGERPRINT.startsWith("generic")
                || Build.FINGERPRINT.startsWith("unknown")
                || Build.MODEL.contains("google_sdk")
                || Build.MODEL.contains("Emulator")
                || Build.MODEL.contains("Android SDK built for x86")
                || Build.MANUFACTURER.contains("Genymotion")
                || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                || "google_sdk" == Build.PRODUCT)
    }
    
    private fun checkAdvanced(): Boolean {
        return (Build.BOARD == "QC_Reference_Phone"
                || Build.BOOTLOADER == "unknown"
                || Build.DEVICE.startsWith("generic")
                || Build.HARDWARE == "ranchu"
                || Build.HARDWARE == "goldfish"
                || Build.MANUFACTURER == "unknown"
                || Build.MODEL == "sdk"
                || Build.MODEL == "google_sdk"
                || Build.PRODUCT == "sdk"
                || Build.PRODUCT == "google_sdk"
                || Build.SERIAL == null)
    }
    
    private fun checkFiles(): Boolean {
        val knownFiles = arrayOf(
            "/dev/socket/qemud",
            "/dev/qemu_pipe",
            "/system/lib/libc_malloc_debug_qemu.so",
            "/sys/qemu_trace",
            "/system/bin/qemu-props"
        )
        
        return knownFiles.any { File(it).exists() }
    }
    
    private fun checkQEmuDrivers(): Boolean {
        val drivers = arrayOf(
            "goldfish",
            "ranchu"
        )
        
        return try {
            val file = File("/proc/tty/drivers")
            if (file.exists() && file.canRead()) {
                val data = file.readText()
                drivers.any { data.contains(it) }
            } else {
                false
            }
        } catch (e: Exception) {
            false
        }
    }
    
    private fun checkIpAddresses(): Boolean {
        val knownIps = arrayOf(
            "10.0.2.15", // Default Android emulator IP
            "10.0.3.2"   // Alternative emulator IP
        )
        
        return try {
            val networkInterfaces = NetworkInterface.getNetworkInterfaces()
            while (networkInterfaces.hasMoreElements()) {
                val networkInterface = networkInterfaces.nextElement()
                val addresses = networkInterface.inetAddresses
                
                while (addresses.hasMoreElements()) {
                    val address = addresses.nextElement()
                    if (!address.isLoopbackAddress && !address.isLinkLocalAddress) {
                        val hostAddress = address.hostAddress
                        if (knownIps.contains(hostAddress)) {
                            return true
                        }
                    }
                }
            }
            false
        } catch (e: Exception) {
            false
        }
    }
}
```

### 3. Debugger Detection

```kotlin
// DebuggerDetector.kt
object DebuggerDetector {
    
    fun isDebuggerAttached(): Boolean {
        return Debug.isDebuggerConnected() || Debug.waitingForDebugger()
    }
    
    fun isDebuggable(context: Context): Boolean {
        return (context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
    }
    
    fun detectTracePid(): Boolean {
        return try {
            val statusFile = File("/proc/self/status")
            val status = statusFile.readText()
            val tracerPid = status.lines()
                .firstOrNull { it.startsWith("TracerPid:") }
                ?.substringAfter("TracerPid:")
                ?.trim()
                ?.toIntOrNull()
            
            tracerPid != null && tracerPid > 0
        } catch (e: Exception) {
            false
        }
    }
    
    // Native anti-debug check
    external fun detectDebuggerNative(): Boolean
    
    init {
        System.loadLibrary("security-lib")
    }
}

// In C++ (security-lib.cpp)
/*
#include <jni.h>
#include <unistd.h>
#include <sys/ptrace.h>

extern "C" JNIEXPORT jboolean JNICALL
Java_com_yourbank_app_security_DebuggerDetector_detectDebuggerNative(
    JNIEnv* env,
    jobject thiz) {
    
    // Try to attach ptrace to ourselves
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
        // Already being traced
        return JNI_TRUE;
    }
    
    // Detach if we successfully attached
    ptrace(PTRACE_DETACH, 0, 0, 0);
    return JNI_FALSE;
}
*/
```

### 4. Screen Security

```kotlin
// ScreenSecurityManager.kt
class ScreenSecurityManager @Inject constructor(
    private val activity: Activity
) {
    
    fun enableScreenSecurity() {
        // Prevent screenshots and screen recording
        activity.window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
    
    fun disableScreenSecurity() {
        activity.window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
    
    fun maskRecentAppsScreenshot() {
        // This should be called when sensitive data is displayed
        enableScreenSecurity()
    }
    
    fun detectScreenRecording(): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            return activity.isInPictureInPictureMode || isScreenBeingRecorded()
        }
        return false
    }
    
    @RequiresApi(Build.VERSION_CODES.Q)
    private fun isScreenBeingRecorded(): Boolean {
        val mediaProjectionManager = activity.getSystemService(
            Context.MEDIA_PROJECTION_SERVICE
        ) as MediaProjectionManager
        
        // Check if any app is recording screen
        // Note: This is limited and may not catch all cases
        return try {
            mediaProjectionManager.getMediaProjection(-1, Intent()) != null
        } catch (e: Exception) {
            false
        }
    }
}

// Compose version
@Composable
fun SecureScreen(content: @Composable () -> Unit) {
    val context = LocalContext.current
    val activity = context.findActivity()
    
    DisposableEffect(Unit) {
        activity?.window?.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
        
        onDispose {
            activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        }
    }
    
    content()
}

fun Context.findActivity(): Activity? {
    var context = this
    while (context is ContextWrapper) {
        if (context is Activity) return context
        context = context.baseContext
    }
    return null
}
```
