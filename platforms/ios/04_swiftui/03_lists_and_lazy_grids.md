# 📜 Lists & Lazy Grids
> **Targeted for iOS Developers**
> **Note:** Performance, Identifiable, and Customization.

![Lists](https://img.shields.io/badge/SwiftUI-Lists-yellow?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. List vs LazyVStack](#1-list-vs-lazyvstack)
- [2. Identifiable Protocol](#2-identifiable)
- [3. Grids](#3-grids)

---

### Q1. `List` vs `LazyVStack` inside `ScrollView`?

**Answer:**
- **`List`**: Uses UITableView/UICollectionView under the hood. Native look & feel (separators, swipe actions). **Lazy loading built-in**.
- **`LazyVStack`**: Just a stack that creates views only when needed. No separators or native styling. Highly customizable layout. Use inside `ScrollView`.

### Q2. Swipe Actions?

**Answer:**
Available on `List` rows.
```swift
.swipeActions(edge: .trailing) {
    Button(role: .destructive) { delete() } label: { Label("Delete", systemImage: "trash") }
}
```

### Q3. `GridItem` configuration?

**Answer:**
Used in `LazyVGrid`.
- **`.fixed(size)`**: Exact size.
- **`.flexible(min, max)`**: Takes available space (standard grid).
- **`.adaptive(minimum)`**: Fits as many items as possible in the row (responsive like Web Flexbox).

### Q4. ScrollTo functionality?

**Answer:**
Wrap the content in a `ScrollViewReader`.
```swift
ScrollViewReader { proxy in
    Button("Jump") { proxy.scrollTo(id, anchor: .top) }
}
```
