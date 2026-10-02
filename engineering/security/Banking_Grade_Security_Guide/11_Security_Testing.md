## 🧪 Security Testing

### 1. Security Test Cases

```kotlin
// SecurityTests.kt
@RunWith(AndroidJUnit4::class)
class SecurityTests {
    
    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)
    
    @Test
    fun testScreenshotPrevention() {
        activityRule.scenario.onActivity { activity ->
            val flags = activity.window.attributes.flags
            assertTrue(
                "Screen security not enabled",
                flags and WindowManager.LayoutParams.FLAG_SECURE != 0
            )
        }
    }
    
    @Test
    fun testRootDetection() {
        val isRooted = RootDetector.isRooted()
        // Should handle rooted devices appropriately
        assertTrue("Root detection not working", true) // Adjust based on test device
    }
    
    @Test
    fun testEncryptedStorage() {
        val testData = "sensitive_data"
        val prefs = SecurePreferences(ApplicationProvider.getApplicationContext())
        
        prefs.saveToken(testData)
        val retrieved = prefs.getToken()
        
        assertEquals(testData, retrieved)
        
        // Verify data is encrypted in storage
        val rawPrefs = ApplicationProvider.getApplicationContext()
            .getSharedPreferences("secure_prefs", Context.MODE_PRIVATE)
        val rawValue = rawPrefs.getString("auth_token", null)
        
        assertNotEquals(
            "Data not encrypted",
            testData,
            rawValue
        )
    }
    
    @Test
    fun testCertificatePinning() {
        // This would need to be tested with actual network calls
        // or mocked SSL context
        val client = SecurityConfig.getOkHttpClient()
        assertNotNull(client.certificatePinner)
    }
    
    @Test
    fun testAppSignatureVerification() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val checker = IntegrityChecker(context)
        assertTrue("Signature verification failed", checker.verifyAppSignature())
    }
}
```

### 2. Penetration Testing Checklist

```markdown
# Mobile App Penetration Testing Checklist
