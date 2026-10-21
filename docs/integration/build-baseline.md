---
type: concept
---

# Build baseline

C# 15 preview is the selected language for the shared backend and official contracts. The SDK includes the compiler; adapters retain their native-language APIs.

## Responsibilities

Use a .NET 11 SDK supporting C# 15 unions and set LangVersion to preview. Pin the exact verified SDK with global.json and allowPrerelease once installation and a union/interface compilation probe pass. SDK installation is coordinated with the PC-reorganization agent. This specification does not claim that the compiler is already installed or that R3CLI has been implemented.

## Rules

- Use native InlineInput and ComponentInput unions for string/component authoring.
- Use params IEnumerable<T> for variadic sequences, with required-first-item or collection overloads where nonempty input is required.
- Preserve validation and identity when using primary constructors, records and extension blocks.
- Verify the interface cases, collection overload resolution and invalid inline inputs with the selected compiler before implementing the backend.
- Execution/distribution mode is independently defined by [[docs/questions/native-aot-or-jit|Native AOT or JIT]].

## Example

```xml
<PropertyGroup>
  <LangVersion>preview</LangVersion>
</PropertyGroup>
```

[Microsoft union prerequisites](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/tutorials/unions) require .NET 11 Preview 5 or later. [SDK downloads](https://dotnet.microsoft.com/en-us/download/dotnet/11.0) provide the compiler. The chosen preview language is a design decision; successful local compiler verification is a build prerequisite.
