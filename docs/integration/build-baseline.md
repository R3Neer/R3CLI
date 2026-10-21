---
type: concept
---

# Build baseline

C# 15 preview is the language for the shared backend and official contracts. The root global.json pins SDK 11.0.100-rc.2.26504.105 with allowPrerelease enabled and rollForward disabled. The SDK supplies the compiler.

## Responsibilities

Use the pinned SDK and LangVersion preview for C# compilation. The verified Windows installation is D:/Program Files/dotnet, with SDKs 10.0.300 and 11.0.100-rc.2.26504.105 coexisting under sdk. This machine path is installation evidence, not a hardcoded build dependency for other machines. R3CLI's native implementation is not part of this documentation update.

## Rules

- Native InlineInput and ComponentInput unions accept interface/string cases at authoring boundaries.
- Use params IEnumerable<T> for variadic sequences; preserve required-first-item/collection overloads for nonempty tables.
- Isolated compiler verification with the pinned SDK has passed interface/string union declarations, conversions from string and an interface-typed variable, and expanded params IEnumerable<union> arguments.
- This probe does not establish every constructor/collection overload, negative compilation case, runtime renderer, adapter or Native AOT behavior. Verify those with implementation-specific tests when that work is authorized.
- Preserve validation, named arguments and identity when applying modern syntax.
- Execution/distribution mode remains independently addressed in [[docs/questions/native-aot-or-jit|Native AOT or JIT]].

## Example

```json
{
  "sdk": {
    "version": "11.0.100-rc.2.26504.105",
    "rollForward": "disable",
    "allowPrerelease": true
  }
}
```

```xml
<PropertyGroup>
  <LangVersion>preview</LangVersion>
</PropertyGroup>
```

Run dotnet --version from the repository root to verify SDK resolution. [Microsoft's union documentation](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/tutorials/unions) describes the preview feature. The pin records a reproducible compiler selection; it does not install an SDK or change the other installed SDK.
