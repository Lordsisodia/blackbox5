---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker",
    "fetched_at": "2026-02-10T13:28:38.684308",
    "status": 200,
    "size_bytes": 254400
  },
  "metadata": {
    "title": "DatePicker",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "datepicker"
  }
}
---

# DatePicker

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# DatePickerAsk assistantDate pickers let merchants choose dates from a visual calendar that’s consistently applied wherever dates need to be selected across Shopify.

## [Anchor to datepickerprops](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops)DatePickerProps[Anchor to defaultYearMonth](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-defaultyearmonth)defaultYearMonth**defaultYearMonth**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**Default [uncontrolled](https://reactjs.org/docs/forms.html#controlled-components) year and month to display. Ignored when year/month navigation is [controlled](https://reactjs.org/docs/forms.html#controlled-components).

[Anchor to disabled](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-disabled)disabled**disabled**DisabledDisabled | DisabledDisabled[] | boolean**DisabledDisabled | DisabledDisabled[] | boolean**Disabled dates, days, and/or ranges, or the date picker. Unbound range disables all dates either from `start` date or to `end` date. `true` disables the date picker.

[Anchor to onChange](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-onchange)onChange**onChange**(selected: T) => void**(selected: T) => void**A callback that is run whenever a date is selected or unselected. This callback is called with a string, an array of strings or a range object representing the selected dates. This component is [controlled](https://reactjs.org/docs/forms.html#controlled-components), so you must store these values in state and reflect it back in the `selected` props.

[Anchor to onYearMonthChange](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-onyearmonthchange)onYearMonthChange**onYearMonthChange**(yearMonth: { year: number; month: number; }) => void**(yearMonth: { year: number; month: number; }) => void**A callback that is run whenever the month is changed. This callback is called with an object indicating the year/month the UI should change to. When year/month navigation is controlled you must store these values in state and reflect it back in the `yearMonth` prop.

[Anchor to readOnly](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-readonly)readOnly**readOnly**boolean**boolean**Whether the date picker is read-only.

[Anchor to selected](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-selected)selected**selected**T**T**A date, an array of dates, or a range object with `start` and/or `end` keys indicating the selected dates. When a range is set, dates between the boundaries will be selected. Passed `undefined` or `string` allows user to select a single date, an empty array or an array of dates allows selecting multiple dates, an empty object or a Range object allows selecting a range of dates.

[Anchor to yearMonth](/docs/api/admin-extensions/2025-07/ui-components/forms/datepicker#datepickerprops-propertydetail-yearmonth)yearMonth**yearMonth**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**{year: YearYear; month: MonthMonth} | YearMonthStringYearMonthString**[Controlled](https://reactjs.org/docs/forms.html#controlled-components) year and month to display. Use in combination with `onYearMonthChange`. Makes year/month navigation [controlled](https://reactjs.org/docs/forms.html#controlled-components).

### Year```

number

```### MonthMonth in 1-12 range```

number

```### YearMonthStringA year/month string using the simplified ISO 8601 format (`YYYY-MM`)```

string

```### Disabled```

DateString | Range | Day

```### DateStringA date string using the simplified ISO 8601 format (`YYYY-MM-DD`)```

string

```### Range- endLast day (inclusive) of the selected range```

DateString

```- startFirst day (inclusive) of the selected range```

DateString

``````

export interface Range {

/**

* First day (inclusive) of the selected range

*/

start?: DateString;

/**

* Last day (inclusive) of the selected range

*/

end?: DateString;

}

```### Day```

'Sunday' | 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday'

```ExamplesAdd a single-date DatePickerReactJSCopy99123456789101112131415import React, { useState } from 'react';import {  render,  DatePicker,  type Selected} from '@shopify/ui-extensions-react/admin';render('Playground', () => <App />);function App() {  const [selected, setSelected] = useState<Selected>('2023-11-08')  return (    <DatePicker selected={selected} onChange={setSelected} />  );}## Preview### Examples- #### Add a single-date DatePickerReact```

import React, { useState } from 'react';

import {

render,

DatePicker,

type Selected

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

const [selected, setSelected] = useState<Selected>('2023-11-08')

return (

<DatePicker selected={selected} onChange={setSelected} />

);

}

```JS```

import {extend, DatePicker} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const datePicker = root.createComponent(

DatePicker,

{},

'DatePicker',

);

root.appendChild(datePicker);

});

```- #### Add a multi-date DatePickerDescriptionUse this when merchants need to select multiple dates.React```

import React from 'react';

import {

render,

DatePicker,

type Selected,

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

const [selected, setSelected] = React.useState<Selected>(['2023-11-08']);

return (

<DatePicker selected={selected} onChange={setSelected} />

);

}

```JS```

import {extend, DatePicker} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const datePicker = root.createComponent(

DatePicker,

{ selected: ['2023-11-08'] },

'DatePicker',

);

root.appendChild(datePicker);

});

```- #### Add a range DatePickerDescriptionUse this when merchants need to select a range of dates.React```

import React from 'react';

import {

render,

DatePicker,

type Selected

} from '@shopify/ui-extensions-react/admin';

render('Playground', () => <App />);

function App() {

const [selected, setSelected] = React.useState<Selected>({start: '2023-11-08', end: '2023-11-10' });

return (

<DatePicker selected={selected} onChange={setSelected} />

);

}

```JS```

import {extend, DatePicker} from '@shopify/ui-extensions/admin';

extend('Playground', (root) => {

const datePicker = root.createComponent(

DatePicker,

{ selected: {start: '2023-11-08', end: '2023-11-10' } },

'DatePicker',

);

root.appendChild(datePicker);

});

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)