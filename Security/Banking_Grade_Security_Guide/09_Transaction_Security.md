## 💰 Transaction Security

### 1. Transaction Signing

```kotlin
// TransactionSigner.kt
class TransactionSigner @Inject constructor(
    private val keystoreManager: KeystoreManager
) {
    
    fun signTransaction(transaction: Transaction): SignedTransaction {
        val transactionData = serializeTransaction(transaction)
        val signature = generateSignature(transactionData)
        
        return SignedTransaction(
            transaction = transaction,
            signature = signature,
            timestamp = System.currentTimeMillis(),
            nonce = UUID.randomUUID().toString()
        )
    }
    
    private fun serializeTransaction(transaction: Transaction): String {
        return buildString {
            append(transaction.fromAccount)
            append("|")
            append(transaction.toAccount)
            append("|")
            append(transaction.amount)
            append("|")
            append(transaction.currency)
            append("|")
            append(transaction.type)
        }
    }
    
    private fun generateSignature(data: String): String {
        val privateKey = keystoreManager.getPrivateKey()
        val signature = Signature.getInstance("SHA256withRSA")
        signature.initSign(privateKey)
        signature.update(data.toByteArray())
        
        val signed = signature.sign()
        return Base64.encodeToString(signed, Base64.NO_WRAP)
    }
    
    fun verifyTransaction(signedTransaction: SignedTransaction): Boolean {
        val publicKey = keystoreManager.getPublicKey()
        val transactionData = serializeTransaction(signedTransaction.transaction)
        
        val signature = Signature.getInstance("SHA256withRSA")
        signature.initVerify(publicKey)
        signature.update(transactionData.toByteArray())
        
        val signatureBytes = Base64.decode(signedTransaction.signature, Base64.NO_WRAP)
        return signature.verify(signatureBytes)
    }
}

data class Transaction(
    val id: String,
    val fromAccount: String,
    val toAccount: String,
    val amount: Double,
    val currency: String,
    val type: TransactionType,
    val description: String?
)

data class SignedTransaction(
    val transaction: Transaction,
    val signature: String,
    val timestamp: Long,
    val nonce: String
)

enum class TransactionType {
    TRANSFER, PAYMENT, WITHDRAWAL, DEPOSIT
}
```

### 2. Transaction Limits & Velocity Checks

```kotlin
// TransactionValidator.kt
class TransactionValidator @Inject constructor(
    private val transactionRepository: TransactionRepository,
    private val accountRepository: AccountRepository
) {
    
    suspend fun validateTransaction(transaction: Transaction): ValidationResult {
        // Check 1: Daily limit
        val dailyLimitCheck = checkDailyLimit(transaction)
        if (!dailyLimitCheck.isValid) {
            return dailyLimitCheck
        }
        
        // Check 2: Single transaction limit
        val singleLimitCheck = checkSingleTransactionLimit(transaction)
        if (!singleLimitCheck.isValid) {
            return singleLimitCheck
        }
        
        // Check 3: Velocity check (frequency)
        val velocityCheck = checkVelocity(transaction)
        if (!velocityCheck.isValid) {
            return velocityCheck
        }
        
        // Check 4: Sufficient balance
        val balanceCheck = checkBalance(transaction)
        if (!balanceCheck.isValid) {
            return balanceCheck
        }
        
        // Check 5: Suspicious pattern detection
        val patternCheck = detectSuspiciousPattern(transaction)
        if (!patternCheck.isValid) {
            return patternCheck
        }
        
        return ValidationResult(true, "Transaction validated successfully")
    }
    
    private suspend fun checkDailyLimit(transaction: Transaction): ValidationResult {
        val startOfDay = LocalDate.now().atStartOfDay()
        val todaysTransactions = transactionRepository.getTransactionsSince(
            transaction.fromAccount,
            startOfDay
        )
        
        val todaysTotal = todaysTransactions.sumOf { it.amount }
        val dailyLimit = accountRepository.getDailyLimit(transaction.fromAccount)
        
        if (todaysTotal + transaction.amount > dailyLimit) {
            return ValidationResult(
                false,
                "Daily transaction limit exceeded. Limit: $dailyLimit, Used: $todaysTotal"
            )
        }
        
        return ValidationResult(true, "Daily limit check passed")
    }
    
    private fun checkSingleTransactionLimit(transaction: Transaction): ValidationResult {
        val singleTransactionLimit = when (transaction.type) {
            TransactionType.TRANSFER -> 50000.0
            TransactionType.PAYMENT -> 25000.0
            TransactionType.WITHDRAWAL -> 10000.0
            TransactionType.DEPOSIT -> Double.MAX_VALUE
        }
        
        if (transaction.amount > singleTransactionLimit) {
            return ValidationResult(
                false,
                "Single transaction limit exceeded. Maximum: $singleTransactionLimit"
            )
        }
        
        return ValidationResult(true, "Single transaction limit check passed")
    }
    
    private suspend fun checkVelocity(transaction: Transaction): ValidationResult {
        val last15Minutes = LocalDateTime.now().minusMinutes(15)
        val recentTransactions = transactionRepository.getTransactionsSince(
            transaction.fromAccount,
            last15Minutes
        )
        
        // Allow max 5 transactions in 15 minutes
        if (recentTransactions.size >= 5) {
            return ValidationResult(
                false,
                "Too many transactions in short period. Please try again later."
            )
        }
        
        return ValidationResult(true, "Velocity check passed")
    }
    
    private suspend fun checkBalance(transaction: Transaction): ValidationResult {
        val account = accountRepository.getAccount(transaction.fromAccount)
        
        if (account.balance < transaction.amount) {
            return ValidationResult(
                false,
                "Insufficient balance. Available: ${account.balance}"
            )
        }
        
        return ValidationResult(true, "Balance check passed")
    }
    
    private suspend fun detectSuspiciousPattern(transaction: Transaction): ValidationResult {
        // Check for round numbers (potential fraud indicator)
        if (transaction.amount % 1000 == 0.0 && transaction.amount > 10000) {
            return ValidationResult(
                false,
                "Transaction requires additional verification",
                requiresStepUpAuth = true
            )
        }
        
        // Check for unusual transaction pattern
        val userHistory = transactionRepository.getUserTransactionHistory(
            transaction.fromAccount,
            limit = 100
        )
        
        val avgAmount = userHistory.map { it.amount }.average()
        
        // If transaction is 5x the average, flag for review
        if (transaction.amount > avgAmount * 5) {
            return ValidationResult(
                false,
                "Unusual transaction amount detected. Additional verification required.",
                requiresStepUpAuth = true
            )
        }
        
        return ValidationResult(true, "Pattern check passed")
    }
}

data class ValidationResult(
    val isValid: Boolean,
    val message: String,
    val requiresStepUpAuth: Boolean = false
)
```

### 3. Step-Up Authentication

```kotlin
// StepUpAuthManager.kt
class StepUpAuthManager @Inject constructor(
    private val biometricManager: BiometricManager,
    private val otpService: OTPService
) {
    
    suspend fun requireStepUpAuth(
        activity: FragmentActivity,
        transaction: Transaction,
        method: StepUpMethod = StepUpMethod.BIOMETRIC
    ): Result<Boolean> {
        return when (method) {
            StepUpMethod.BIOMETRIC -> authenticateWithBiometric(activity, transaction)
            StepUpMethod.PIN -> authenticateWithPIN(transaction)
            StepUpMethod.OTP -> authenticateWithOTP(transaction)
        }
    }
    
    private suspend fun authenticateWithBiometric(
        activity: FragmentActivity,
        transaction: Transaction
    ): Result<Boolean> {
        return suspendCoroutine { continuation ->
            biometricManager.authenticateWithCrypto(
                activity,
                onSuccess = { cipher ->
                    // Use authenticated cipher to encrypt transaction
                    continuation.resume(Result.success(true))
                },
                onError = { code, message ->
                    continuation.resume(
                        Result.failure(Exception("Biometric auth failed: $message"))
                    )
                }
            )
        }
    }
    
    private suspend fun authenticateWithPIN(transaction: Transaction): Result<Boolean> {
        // Show PIN dialog and verify
        // Implementation depends on UI framework
        return Result.success(true)
    }
    
    private suspend fun authenticateWithOTP(transaction: Transaction): Result<Boolean> {
        return try {
            val otpSent = otpService.sendTransactionOTP(transaction)
            if (otpSent) {
                Result.success(true)
            } else {
                Result.failure(Exception("Failed to send OTP"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

enum class StepUpMethod {
    BIOMETRIC, PIN, OTP
}
```
