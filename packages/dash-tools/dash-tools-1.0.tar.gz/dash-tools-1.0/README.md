# 🛠️ **dash-tools** - _Easily Create and Deploy your Plotly Dash Apps from CLI (🎉 V1.0)_

Create a templated multi-page [Plotly Dash](https://plotly.com/dash/) app with CLI in less than 7 seconds.

Deploy your app to [Heroku](https://heroku.com/) in under a minute!

![](docs/intro_gif.gif)

## **About**

[**dash-tools**](https://github.com/andrew-hossack/dash-tools) is an open-source toolchain for [Plotly Dash Framework](https://dash.plotly.com/introduction). With a user-friendly command line interface, creating Dash applications has never been quicker.

Includes user and developer-friendly app templates where generating a new app only takes seconds. In fact, it will take longer to install this tool than it will to use it!

Want to deploy your app to the web? We've got you covered. With [Heroku](https://heroku.com/) support, deploying your project will take under a minute.

## **Installation**

Ready to use **dash-tools**? Installation is easy with pip:

```bash
pip install dash-tools
```

[Find dash-tools on PyPi](https://pypi.org/project/dash-tools/)

## **Usage Examples**

Below are common usage examples. For a more in-depth tutorial on writing apps for Plotly Dash, see the [Plotly Dash Documentation](https://dash.plotly.com/layout). For information about dash-tools commands, read the [_Commands_](#commands) section.

### **Creating A New Project**

Creating a new Dash project is very simple. The following command will create a new directory called "MyDashApp" using the optional "multipage" template. Learn more about [_Templates_](#templates) below.

```bash
dash-tools --init MyDashApp multipage
```

Optionally, no template needs to be specified. Instead, the 'default' template will be used:

```bash
dash-tools --init MyDashApp
```

The previous command will create a "MyDashApp" directory. You can see what files are included with your new app:

```bash
cd MyDashApp && ls
```

You can make changes to your app in the src/app.py file! See [https://dash.plotly.com/layout](https://dash.plotly.com/layout) for more information.

When you are happy with your changes, run your dash app locally with the following command. You will be able to view your app at http://127.0.0.1:8050/ in your browser:

```bash
python src/app.py
```

### **Deploying To Heroku**

Deploying your project online to [Heroku](https://www.heroku.com/) is simple. The CLI handles both creating and deploying a new app, as well as updating an existing app.

#### **Creating a Heroku App**

To create an app, run the following command from your project's root directory; e.g. _/MyDashApp_ from the example above. Next, follow the simple on-screen directions and deployment will be handled for you:

```bash
dash-tools --deploy-heroku
```

Optionally, you can specify a heroku app name as an argument. If one is not provided, you will be prompted to enter one or generate one automatically.

_Note that "some-unique-heroku-app-name" in the example below is a name that you should change._

```bash
dash-tools --deploy-heroku some-unique-heroku-app-name
```

And that's really it! You will be prompted to log into your heroku account, a git remote 'heroku' will be created and changes will be pushed and deployed automatically.

#### **Pushing Changes to an Existing Heroku App**

To push changes to an existing heroku app after it is deployed, you can use the same command as before. Since a 'heroku' git remote already exists, by choosing the on-screen option to "Update Existing App", all changes will be pushed and your app will be re-deployed:

```bash
dash-tools --deploy-heroku
```

If you would rather add specific files, make a commit and push to the 'heroku' remote manually:

```bash
git add SomeFileYouModified.txt
git commit -m "Your Commit Message"
git push heroku
```

## **Templates**

Templates contain boilerplate code for Dash projects, making it much easier to start with useful baseline apps.

### **Using Templates**

Use the optional template argument with the `--init` command.

The following example will create a new app "MyWonderfulApp" (you can name your app anything) using the 'tabs' template (or any other template listed below):

```bash
dash-tools --init MyWonderfulApp tabs
```

To list out available templates, use the `--templates` or `-t` command:

```bash
dash-tools --templates
```

### **Available Templates**

_Click the dropdowns below to see screenshots!_

<details><summary>Template: 'advanced'</summary>

Advanced multi-page template. Includes examples of ClientsideCallbacks, multi-page routing, external stylesheets, header, footer, and 404 page.
![](docs/advanced_theme.png)

</details>

<details><summary>Template: 'default'</summary>

Basic Dash template. See [Dash Docs](https://dash.plotly.com/layout)
![](docs/default_theme.png)

</details>

<details><summary>Template: 'iris'</summary>

Iris theme. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/)
![](docs/iris_theme.png)

</details>

<details><summary>Template: 'mantine'</summary>

Basic mantine template. See [Dash Mantine](https://www.dash-mantine-components.com/)
![](docs/mantine_theme.png)

</details>

<details><summary>Template: 'multipage'</summary>

New multipage theme. See [Multipage Plugin](https://github.com/plotly/dash-labs/blob/main/docs/08-MultiPageDashApp.md)
![](docs/multipage_new_theme.png)

</details>

<details><summary>Template: 'sidebar'</summary>

Sidebar theme. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/)
![](docs/sidebar_theme.png)

</details>

<details><summary>Template: 'tabs'</summary>

Tabs theme with dynamically generated content. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/)
![](docs/tabs_theme.png)

</details>

## **Commands**

### **Project Commands**

- **`--deploy-heroku` Args: OPTIONAL (`unique heroku project name`) :** Deploys the project to Heroku using the [Heroku CLI](https://devcenter.heroku.com/categories/command-line) (Must Install Seperately) and [Git](https://git-scm.com/downloads). Invoke from the project root directory.
- **`--init, -i` Args: REQUIRED (`project name`) OPTIONAL (`template`) :** Creates a Plotly Dash app with the given name in the current working directory. Optional args specified can be used for templates.
- **`--templates, -t` :** List available templates.

### Other

- **`--help, -h`:** Display CLI helpful hints
- **`--version`:** Display current version.

## **Development**

### **Creating Templates**

1. Templates are found here: `dash_tools/templating/templates/<Template Name>`. When a user uses CLI to choose a template with the name `<Template Name>` the template will be copied to their system.
2. Adding a new template to the templates directory requires adding the new template to the Enum list in `templating.Templates` Enum. Template name must match Enum value, eg.

   ```python
   class Templates(Enum):
      DEFAULT = 'default'
      MINIMAL = 'minimal'
      NEWTEMPLATE = 'newtemplate'
   ```

3. Any file names or files containing the strings `{appName}` or `{createTime}` will be formatted with the given app name and creation time. Eg. _README.md.template_: `# Created on {createTime}` will copy to the user's filesystem as _README.md_: `# Created on 2022-03-30 22:06:07`
4. All template files must end in `.template`

## **License**

MIT License. See LICENSE.txt file.
