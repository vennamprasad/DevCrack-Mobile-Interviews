## **Navigation**

### 20. How does Navigation work in Compose?

**Answer:**
Compose Navigation uses `NavHost` and `NavController` to navigate between composable screens.

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(onNavigateToDetail = { id ->
                navController.navigate("detail/$id")
            })
        }
        composable(
            route = "detail/{id}",
            arguments = listOf(navArgument("id") { type = NavType.IntType })
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("id")
            DetailScreen(id = id)
        }
    }
}
```

---

### 21. How to pass arguments in Compose Navigation?

**Answer:**
Use route placeholders and navArguments.

```kotlin
// Define route with argument
composable(
    route = "profile/{userId}",
    arguments = listOf(
        navArgument("userId") {
            type = NavType.StringType
            nullable = false
        }
    )
) { backStackEntry ->
    val userId = backStackEntry.arguments?.getString("userId")
    ProfileScreen(userId = userId!!)
}

// Navigate with argument
navController.navigate("profile/$userId")
```

**For complex objects, use:**
- JSON serialization
- Shared ViewModel
- SavedStateHandle
