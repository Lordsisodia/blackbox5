---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/datefield",
    "fetched_at": "2026-02-10T13:29:45.071277",
    "status": 200,
    "size_bytes": 325203
  },
  "metadata": {
    "title": "DateField",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "datefield"
  }
}
---

# DateField

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# DateFieldAsk assistantAllow users to select a specific date with a date picker.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties)Properties[Anchor to allow](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-allow)allow**allow**string**string**Default: ""**Default: ""**Dates that can be selected.

A comma-separated list of dates, date ranges. Whitespace is allowed after commas.

The default `''` allows all dates.

- Dates in `YYYY-MM-DD` format allow a single date.

- Dates in `YYYY-MM` format allow a whole month.

- Dates in `YYYY` format allow a whole year.

- Ranges are expressed as `start--end`.     - Ranges are inclusive.

If either `start` or `end` is omitted, the range is unbounded in that direction.

- If parts of the date are omitted for `start`, they are assumed to be the minimum possible value.

So `2024--` is equivalent to `2024-01-01--`.

- If parts of the date are omitted for `end`, they are assumed to be the maximum possible value.

So `--2024` is equivalent to `--2024-12-31`.

- Whitespace is allowed either side of `--`.

[Anchor to allowDays](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-allowdays)allowDays**allowDays**string**string**Default: ""**Default: ""**Days of the week that can be selected. These intersect with the result of `allow` and `disallow`.

A comma-separated list of days. Whitespace is allowed after commas.

The default `''` has no effect on the result of `allow` and `disallow`.

Days are `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`.

[Anchor to autocomplete](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-autocomplete)autocomplete**autocomplete**DateAutocompleteFieldDateAutocompleteField**DateAutocompleteFieldDateAutocompleteField**Default: 'on' for everything else**Default: 'on' for everything else**A hint as to the intended content of the field.

When set to `on` (the default), this property indicates that the field should support autofill, but you do not have any more semantic information on the intended contents.

When set to `off`, you are indicating that this field contains sensitive information, or contents that are never saved, like one-time codes.

Alternatively, you can provide value which describes the specific data you would like to be entered into this field during autofill.

[Anchor to defaultValue](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-defaultvalue)defaultValue**defaultValue**string**string**The default value for the field.

[Anchor to defaultView](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-defaultview)defaultView**defaultView**string**string**Default month to display in `YYYY-MM` format.

This value is used until `view` is set, either directly or as a result of user interaction.

Defaults to the current month in the user's locale.

[Anchor to details](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-details)details**details**string**string**Additional text to provide context or guidance for the field. This text is displayed along with the field and its label to offer more information or instructions to the user.

This will also be exposed to screen reader users.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to disallow](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-disallow)disallow**disallow**string**string**Default: ""**Default: ""**Dates that cannot be selected. These subtract from `allow`.

A comma-separated list of dates, date ranges. Whitespace is allowed after commas.

The default `''` has no effect on `allow`.

- Dates in `YYYY-MM-DD` format disallow a single date.

- Dates in `YYYY-MM` format disallow a whole month.

- Dates in `YYYY` format disallow a whole year.

- Ranges are expressed as `start--end`.     - Ranges are inclusive.

If either `start` or `end` is omitted, the range is unbounded in that direction.

- If parts of the date are omitted for `start`, they are assumed to be the minimum possible value.

So `2024--` is equivalent to `2024-01-01--`.

- If parts of the date are omitted for `end`, they are assumed to be the maximum possible value.

So `--2024` is equivalent to `--2024-12-31`.

- Whitespace is allowed either side of `--`.

[Anchor to disallowDays](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-disallowdays)disallowDays**disallowDays**string**string**Default: ""**Default: ""**Days of the week that cannot be selected. This subtracts from `allowDays`, and intersects with the result of `allow` and `disallow`.

A comma-separated list of days. Whitespace is allowed after commas.

The default `''` has no effect on `allowDays`.

Days are `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to id](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-id)id**id**string**string**A unique identifier for the element.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to placeholder](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-placeholder)placeholder**placeholder**string**string**A short hint that describes the expected value of the field.

[Anchor to readOnly](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Default: false**Default: false**The field cannot be edited by the user. It is focusable will be announced by screen readers.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-value)value**value**string**string**The current value for the field. If omitted, the field will be empty.

[Anchor to view](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#properties-propertydetail-view)view**view**string**string**Displayed month in `YYYY-MM` format.

`onViewChange` is called when this value changes.

Defaults to `defaultView`.

### DateAutocompleteField```

'bday-day' | 'bday-month' | 'bday-year' | 'bday' | 'cc-expiry-month' | 'cc-expiry-year' | 'cc-expiry'

```## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to blur](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-blur)blur**blur**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to focus](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-focus)focus**focus**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<'input'>**CallbackEventListenerCallbackEventListener<'input'>**[Anchor to invalid](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-invalid)invalid**invalid**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**[Anchor to viewchange](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#events-propertydetail-viewchange)viewchange**viewchange**CallbackEventListenerCallbackEventListener<typeof tagName> | null**CallbackEventListenerCallbackEventListener<typeof tagName> | null**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy91<s-date-field defaultView="2025-09" defaultValue="2025-09-01" />## Preview### Examples- #### Codejsx```

<s-date-field defaultView="2025-09" defaultValue="2025-09-01" />

```html```

<s-date-field defaultView="2025-09" defaultValue="2025-09-01"></s-date-field>

```- #### Basic usageDescriptionSimple date field for collecting a single date with a descriptive label.jsx```

<s-date-field

label="Order date"

name="orderDate"

placeholder="Select date"

/>

```html```

<s-date-field

label="Order date"

name="orderDate"

placeholder="Select date"

></s-date-field>

```- #### With default valueDescriptionDate field pre-populated with a specific date for editing existing data.jsx```

<s-date-field

label="Shipping date"

name="shippingDate"

value="2024-03-15"

/>

```html```

<s-date-field

label="Shipping date"

name="shippingDate"

value="2024-03-15"

></s-date-field>

```- #### With date restrictionsDescriptionShows how to restrict selectable dates to weekdays only.jsx```

<s-date-field

label="Delivery date"

name="deliveryDate"

disallowDays="[0, 6]"

details="Delivery available Monday through Friday only"

/>

```html```

<s-date-field

label="Delivery date"

name="deliveryDate"

disallowDays="[0, 6]"

details="Delivery available Monday through Friday only"

></s-date-field>

```- #### With specific allowed datesDescriptionDemonstrates allowing only specific dates from a predefined list.jsx```

<s-date-field

label="Available appointment dates"

name="appointmentDate"

allow='["2024-03-20", "2024-03-22", "2024-03-25", "2024-03-27"]'

details="Select from available time slots"

/>

```html```

<s-date-field

label="Available appointment dates"

name="appointmentDate"

allow='["2024-03-20", "2024-03-22", "2024-03-25", "2024-03-27"]'

details="Select from available time slots"

></s-date-field>

```- #### With error stateDescriptionDate field showing validation error for required field or invalid date entry.jsx```

<s-date-field

label="Event date"

error="Event date is required"

required

/>

```html```

<s-date-field

label="Event date"

name="eventDate"

required

error="Select a valid event date"

></s-date-field>

```- #### Disabled and read-only statesDescriptionShows date fields in different interaction states for viewing-only or disabled forms.jsx```

<s-stack gap="base">

<s-date-field

label="Creation date"

name="createdDate"

value="2024-01-01"

readOnly

/>

<s-date-field

label="Archived date"

name="archivedDate"

value="2024-02-15"

disabled

/>

</s-stack>

```html```

<s-stack gap="base">

<s-date-field

label="Creation date"

name="createdDate"

value="2024-01-01"

readOnly

></s-date-field>

<s-date-field

label="Archived date"

name="archivedDate"

value="2024-02-15"

disabled

></s-date-field>

</s-stack>

```- #### Form integrationDescriptionComplete form example showing date field with other form elements.jsx```

<form>

<s-stack gap="base">

<s-text-field

label="Customer name"

name="customerName"

required

/>

<s-date-field

label="Order date"

name="orderDate"

value="2024-03-15"

required

/>

<s-date-field

label="Requested delivery date"

name="deliveryDate"

disallowDays="[0, 6]"

details="Weekdays only"

/>

<s-button type="submit" variant="primary">

Process order

</s-button>

</s-stack>

</form>

```html```

<form>

<s-stack gap="base">

<s-text-field

label="Customer name"

name="customerName"

required

></s-text-field>

<s-date-field

label="Order date"

name="orderDate"

value="2024-03-15"

required

></s-date-field>

<s-date-field

label="Requested delivery date"

name="deliveryDate"

disallowDays="[0, 6]"

details="Weekdays only"

></s-date-field>

<s-button type="submit" variant="primary">Process order</s-button>

</s-stack>

</form>

```- #### Date range selectionDescriptionExample showing two date fields for selecting a date range.jsx```

<s-stack gap="base">

<s-heading>Sales report period</s-heading>

<s-stack direction="inline" gap="base">

<s-date-field

label="Start date"

name="startDate"

id="report-start"

/>

<s-date-field

label="End date"

name="endDate"

id="report-end"

/>

</s-stack>

<s-button variant="primary">Generate report</s-button>

</s-stack>

```html```

<s-stack gap="base">

<s-heading>Sales report period</s-heading>

<s-stack direction="inline" gap="base">

<s-date-field

label="Start date"

name="startDate"

id="report-start"

></s-date-field>

<s-date-field

label="End date"

name="endDate"

id="report-end"

></s-date-field>

</s-stack>

<s-button variant="primary">Generate report</s-button>

</s-stack>

```- #### Date fields with validationDescriptionDemonstrates date fields with business logic restrictions and validation.jsx```

<s-section>

<s-heading>Promotion settings</s-heading>

<s-stack gap="base">

<s-text-field

label="Promotion name"

name="promoName"

value="Spring sale"

/>

<s-date-field

label="Start date"

name="promoStart"

value="2024-04-01"

details="Promotion begins at midnight"

/>

<s-date-field

label="End date"

name="promoEnd"

value="2024-04-30"

details="Promotion ends at 11:59 PM"

/>

<s-checkbox

name="autoPublish"

label="Automatically publish on start date"

/>

</s-stack>

</s-section>

```html```

<s-section>

<s-heading>Promotion settings</s-heading>

<s-stack gap="base">

<s-text-field

label="Promotion name"

name="promoName"

value="Spring sale"

></s-text-field>

<s-date-field

label="Start date"

name="promoStart"

value="2024-04-01"

details="Promotion begins at midnight"

></s-date-field>

<s-date-field

label="End date"

name="promoEnd"

value="2024-04-30"

details="Promotion ends at 11:59 PM"

></s-date-field>

<s-checkbox

name="autoPublish"

label="Automatically publish on start date"

></s-checkbox>

</s-stack>

</s-section>

```- #### Date field validationDescriptionInteractive example showing required date field validation with dynamic error messages.jsx```

const [date, setDate] = useState('');

const [error, setError] = useState('Event date is required');

return (

<s-section>

<s-stack gap="base" justifyContent="start">

<s-text-field label="Event name" />

<s-date-field

label="Event date"

value={date}

error={error}

required

onChange={(e) => {

setDate(e.currentTarget.value);

setError(e.currentTarget.value ? '' : 'Event date is required');

}}

/>

</s-stack>

</s-section>

)

```html```

<s-date-field

label="Event date"

name="eventDate"

required

error="Select a valid event date"

></s-date-field>

```## [Anchor to best-practices](/docs/api/admin-extensions/latest/polaris-web-components/forms/datefield#best-practices)Best practices

- Use smart defaults and highlight common selections

- Use `allow` and `disallow` properties to restrict selectable dates appropriately

- Provide clear labels and use details text to explain date restrictions

- Don't use for dates that are many years in the future or the past

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)