## 仓库grunt使用说明

### grunt 安装

> Grunt运行离不开NodeJS和NPM。因此要使用Grunt首要的条件，你的系统需要安装NodeJS和NPM。

> 简单的了解一下NodeJS的安装

> node安装的方法很多，如果是wiondow系统,可以直接进入Nodejs官网中[下载](http://nodejs.org/download/)各系统所需要的安装包进行安装。

### 安装NPM

    装好NodeJS后，可以在你的终端执行下面的命令安装NPM:

    curl http://npmjs.org/install.sh | sh

    如果这样安装失败，或许你要在上面的命令之前加上sudo，并按提示输入你的用户密码。

    如果需要检验安装NodeJS或NPM是否要成功，可以通过下面的命令来检验：

    $ node -v
    v0.10.13

    $ npm -v
    1.3.2

> 这样你的NodeJS和NPM表示安装成功。


### 安装CLI

> 为了方便使用Grunt，你应该在全局范围内安装Grunt的命令行接口(CLI)。要做到这一点，需要在命令行中执行：

    $ npm install -g grunt-cli

> 这条命令将会把grunt命令植入到你的系统路径中，这样就允许你从任意目录中运行Grunt(定位到任意目录运行grunt命令)

### 运行grunt
> 进入到Gruntfile.js的目录,在命令行执行：

    $ npm install

> 等待命令执行后，再执行:

    $ grunt

> 即可把要压缩处理的文件处理到Gruntfile.js配置的目录
> 前端开发同学在开发过程中不需要每次都运行上面的grunt命令，可以在命令行运行一个：

    $ grunt dev

> 即可时时监听修改过的文件。

## 本仓库前端开发代码结构说明
    注：本仓库grunt配置文件只须要修改tasks下的两个js文件。less.js配置css文件;concat.js配置js文件。详细操作如下：

**development**

    日常开发的目录，也是开发同学要去修改，添加文件组织的目录。其下有javascripts目录与stylesheets目录。

> **javascripts目录是存放页面js 逻辑的目录**
    其下build目录libs目录是pielAdmin框架的逻辑依赖文件，为保证框架干净，这两个目录一般不需要增删改等操作，如需要有新的插件逻辑增加，请放在libs目录下。
> **sourcess目录是开发者要关心的目录**
    其下components、libs、plugins、目录一般也不需要增删改操作。可以在sourcess下直接新建js文件。也可以新建一个项目页面功能的文件夹后在其内新建js文件（推荐这么做如：htyun）。
  > **sourcess直接新建js文件** 后，需要去tasks目录concat.js文件中files数组里新增加配置片段，（例如：test.js）
  > **sourcess 下新增htyun目录操作实例**
    需要去tasks目录concat.js文件中files数组里新增加配置片段,如果代码有依赖关系，把被依赖的文件放在依赖文件的后面，如例中a.js 与 b.js


    stylesheets说明


> **stylesheets目录是存放页面css的目录**
    stylesheets是存放第三方插件css与项目开发中的CSS文件。目录结构与javascripts相同。
     第三方插件CSS存放在libs目录中。一般不需要修改
     pixel-admin-less目录是pixelAdmin的依赖css。一般不需要修改。

> **stylesheets下直接建css文件**后,
    需要去tasks目录less.js文件中files数组新增加配置片段，（如test.less）

> **stylesheets 下新增htyun目录操作实例**
    需要去tasks目录 less.js文件中files数组中新增加配置片段，一般css没有依赖关系，可以参考htyun的配置，如有依赖关系 可以参考js的依赖疯关系配置。

## OVER
    上面的操作都已经配置好了，就可以专心的写代码了。不想每次都运行grunt，就在控制台直接运行： grunt dev















