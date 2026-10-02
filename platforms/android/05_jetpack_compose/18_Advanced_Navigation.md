## **Advanced Navigation**

### 57. How to implement nested navigation?

**Answer:**

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = "main") {
        composable("main") {
            MainScreen(
                onNavigateToProfile = { navController.navigate("profile") }
            )
        }

        // Nested navigation graph
        navigation(startDestination = "profile/details", route = "profile") {
            composable("profile/details") {
                ProfileDetailsScreen(
                    onNavigateToSettings = {
                        navController.navigate("profile/settings")
                    }
                )
            }
            composable("profile/settings") {
                SettingsScreen()
            }
        }
    }
}
```

---

### 58. How to handle deep links in Compose Navigation?

**Answer:**

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = "home") {
        composable(
            route = "product/{productId}",
            arguments = listOf(
                navArgument("productId") { type = NavType.IntType }
            ),
            deepLinks = listOf(
                navDeepLink {
                    uriPattern = "myapp://product/{productId}"
                    action = Intent.ACTION_VIEW
                },
                navDeepLink {
                    uriPattern = "https://myapp.com/product/{productId}"
                }
            )
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId")
            ProductScreen(productId)
        }
    }
}

// In AndroidManifest.xml
/*
<activity>
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" android:host="product" />
        <data android:scheme="https" android:host="myapp.com" />
    </intent-filter>
</activity>
*/
```

---

### 59. How to implement bottom navigation with multiple back stacks?

**Answer:**

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()
    var selectedTab by rememberSaveable { mutableStateOf(0) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                BottomNavItem.values().forEachIndexed { index, item ->
                    NavigationBarItem(
                        selected = selectedTab == index,
                        onClick = {
                            selectedTab = index
                            navController.navigate(item.route) {
                                // Pop to start destination
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                // Avoid multiple copies
                                launchSingleTop = true
                                // Restore state
                                restoreState = true
                            }
                        },
                        icon = { Icon(item.icon, item.label) },
                        label = { Text(item.label) }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(
            navController,
            startDestination = BottomNavItem.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(BottomNavItem.Home.route) { HomeScreen() }
            composable(BottomNavItem.Search.route) { SearchScreen() }
            composable(BottomNavItem.Profile.route) { ProfileScreen() }
        }
    }
}

enum class BottomNavItem(val route: String, val icon: ImageVector, val label: String) {
    Home("home", Icons.Default.Home, "Home"),
    Search("search", Icons.Default.Search, "Search"),
    Profile("profile", Icons.Default.Person, "Profile")
}
```
