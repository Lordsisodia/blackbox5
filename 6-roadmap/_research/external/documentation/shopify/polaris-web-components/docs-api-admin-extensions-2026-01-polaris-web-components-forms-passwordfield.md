---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/passwordfield",
    "fetched_at": "2026-02-10T13:30:02.078579",
    "status": 200,
    "size_bytes": 290537
  },
  "metadata": {
    "title": "PasswordField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "passwordfield"
  }
}
---

# PasswordField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# PasswordFieldAsk assistantSecurely collect sensitive information from users.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties)Properties[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-autocomplete)autocomplete**autocomplete**"on" | "off" | PasswordAutocompleteFieldPasswordAutocompleteField | `section-${string} current-password` | `section-${string} new-password` | "shipping current-password" | "shipping new-password" | "billing current-password" | "billing new-password" | `section-${string} shipping current-password` | `section-${string} shipping new-password` | `section-${string} billing current-password` | `section-${string} billing new-password`**"on" | "off" | PasswordAutocompleteFieldPasswordAutocompleteField | `section-${string} current-password` | `section-${string} new-password` | "shipping current-password" | "shipping new-password" | "billing current-password" | "billing new-password" | `section-${string} shipping current-password` | `section-${string} shipping new-password` | `section-${string} billing current-password` | `section-${string} billing new-password`**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to maxLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-maxlength)maxLength**maxLength**number**number**Default: Infinity**Default: Infinity**Specifies the maximum number of characters allowed.

[Anchor to minLength](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-minlength)minLength**minLength**number**number**Default: 0**Default: 0**Specifies the min number of characters allowed.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

### PasswordAutocompleteField```

'current-password' | 'new-password'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/passwordfield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy9123456<s-password-field  label="Password"  placeholder="Enter your password"  details="Must be at least 8 characters long"  minLength={8} />## Preview### Examples- #### Codejsx```

<s-password-field

label="Password"

placeholder="Enter your password"

details="Must be at least 8 characters long"

minLength={8}

/>

```html```

<s-password-field

label="Password"

placeholder="Enter your password"

details="Must be at least 8 characters long"

minLength="8"

></s-password-field>

```- #### Basic usageDescriptionDemonstrates a basic password field with a label, name, and required validation. Sets a minimum length of 8 characters and configures autocomplete for a new password.jsx```

<s-password-field

label="Password"

name="password"

required

minLength={8}

autocomplete="new-password"

/>

```html```

<s-password-field

label="Password"

name="password"

required

minLength="8"

autocomplete="new-password"

></s-password-field>

```- #### With error stateDescriptionShows a password field in an error state, displaying a custom error message when the password does not meet the minimum length requirement.jsx```

<s-password-field

label="Password"

name="password"

error="Password must be at least 8 characters"

minLength={8}

autocomplete="new-password"

/>

```html```

<s-password-field

label="Password"

name="password"

error="Password must be at least 8 characters"

minLength="8"

autocomplete="new-password"

></s-password-field>

```- #### With helper textDescriptionIllustrates a password field with additional details providing guidance about password creation requirements.jsx```

<s-password-field

label="Create password"

name="new-password"

details="Password must be at least 8 characters and include uppercase, lowercase, and numbers"

minLength={8}

autocomplete="new-password"

/>

```html```

<s-password-field

label="Create password"

name="new-password"

details="Password must be at least 8 characters and include uppercase, lowercase, and numbers"

minLength="8"

autocomplete="new-password"

></s-password-field>

```- #### In form layoutDescriptionShows how the password field can be integrated into a form alongside other input fields, such as an email field, to create a complete login or registration form.jsx```

<s-stack gap="base">

<s-email-field

label="Email"

name="email"

autocomplete="email"

required

/>

<s-password-field

label="Password"

name="password"

autocomplete="current-password"

required

/>

</s-stack>

```html```

<s-stack gap="base">

<s-email-field

label="Email"

name="email"

autocomplete="username"

required

></s-email-field>

<s-password-field

label="Password"

name="password"

autocomplete="current-password"

required

></s-password-field>

</s-stack>

```- #### With password strength requirementsDescriptionDemonstrates a password field with dynamic password strength validation, showing real-time feedback on password complexity requirements.jsx```

<s-stack gap="large-100">

<s-password-field

label="Create password"

name="password"

value="example-password"

autocomplete="new-password"

required

/>

<s-stack gap="small-200">

<s-text tone="success">✓ At least 8 characters</s-text>

<s-text color="subdued">○ Contains uppercase letter</s-text>

<s-text color="subdued">○ Contains lowercase letter</s-text>

<s-text color="subdued">○ Contains number</s-text>

</s-stack>

</s-stack>

```html```

<s-stack gap="large-100">

<s-password-field

label="Create password"

name="password"

value="example-password"

autocomplete="new-password"

required

></s-password-field>

<s-stack gap="small-200">

<s-text tone="success">✓ At least 8 characters</s-text>

<s-text color="subdued">○ Contains uppercase letter</s-text>

<s-text color="subdued">○ Contains lowercase letter</s-text>

<s-text color="subdued">○ Contains number</s-text>

</s-stack>

</s-stack>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)