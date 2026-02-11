---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction",
    "fetched_at": "2026-02-10T13:29:03.314459",
    "status": 200,
    "size_bytes": 242284
  },
  "metadata": {
    "title": "AdminAction",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "settings-and-templates",
    "component": "adminaction"
  }
}
---

# AdminAction

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2025-07# AdminActionAsk assistantAdminAction is a component used by Admin action extensions to configure a primary and secondary action and title. Use of this component is required in order to use Admin action extensions.

## [Anchor to adminactionprops](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#adminactionprops)AdminActionProps[Anchor to loading](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#adminactionprops-propertydetail-loading)loading**loading**boolean**boolean**Sets the loading state of the action modal

[Anchor to primaryAction](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#adminactionprops-propertydetail-primaryaction)primaryAction**primaryAction**RemoteFragment**RemoteFragment**Sets the Primary action button of the container. This component must be a button component.

[Anchor to secondaryAction](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#adminactionprops-propertydetail-secondaryaction)secondaryAction**secondaryAction**RemoteFragment**RemoteFragment**Sets the Secondary action button of the container. This component must be a button component.

[Anchor to title](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#adminactionprops-propertydetail-title)title**title**string**string**Sets the title of the Action container. If not provided, the name of the extension will be used. Titles longer than 40 characters will be truncated.

ExamplesSet the primary and secondary action of the Action modal.ReactJSCopy99123456789101112131415161718192021222324252627282930import React from 'react';import {  reactExtension,  AdminAction,  Button,  Text,} from '@shopify/ui-extensions-react/admin';function App() {  return (    <AdminAction      title="My App Action"      primaryAction={        <Button onPress={() => {}}>Action</Button>      }      secondaryAction={        <Button onPress={() => {}}>          Secondary        </Button>      }    >      <Text>Modal content</Text>    </AdminAction>  );}export default reactExtension(  'Playground',  () => <App />,);## Preview### Examples- #### Set the primary and secondary action of the Action modal.React```

import React from 'react';

import {

reactExtension,

AdminAction,

Button,

Text,

} from '@shopify/ui-extensions-react/admin';

function App() {

return (

<AdminAction

title="My App Action"

primaryAction={

<Button onPress={() => {}}>Action</Button>

}

secondaryAction={

<Button onPress={() => {}}>

Secondary

</Button>

}

>

<Text>Modal content</Text>

</AdminAction>

);

}

export default reactExtension(

'Playground',

() => <App />,

);

```JS```

import {extension, AdminAction, Button} from '@shopify/ui-extensions/admin';

export default extension('Playground', (root) => {

const primaryAction = root.createFragment();

const secondaryAction = root.createFragment();

primaryAction.appendChild(

root.createComponent(Button, {onPress: () => {}}, 'Action')

);

secondaryAction.appendChild(

root.createComponent(Button, {onPress: () => {}}, 'Secondary')

);

const adminAction = root.createComponent(AdminAction, {

title: 'My App Action',

primaryAction,

secondaryAction,

}, 'Modal content');

root.appendChild(adminAction);

root.mount();

});

```## [Anchor to related](/docs/api/admin-extensions/2025-07/ui-components/settings-and-templates/adminaction#related)Related[AdminBlockAdminBlock](/docs/api/admin-extensions/components/other/adminblock)[ - AdminBlock](/docs/api/admin-extensions/components/other/adminblock)Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)