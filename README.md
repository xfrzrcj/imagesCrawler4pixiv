# imagesCrawler4pixiv
pixiv站图片下载工具

帮朋友写的一个工具，根据指定的id下载www.pixiv.net对应id的插画集

完整可运行组件见百度云链接：https://pan.baidu.com/s/1vavS-0R02JMUaEmU8_pVUw 密码：vi48

食用说明：

例如https://www.pixiv.net/search.php?word=gundam   页面的,想获取如下图红圈所示id，

![image](https://github.com/xfrzrcj/imagesCrawler4pixiv/images/example1.png)

右键图片检查元素获得 <div alt="" class="_309ad3C" style="width: 198px; height: 132px; background-image: url(&quot;https://i.pximg.net/c/240x240/img-master/img/2018/04/26/08/52/22/68409293_p0_master1200.jpg&quot;);"></div>

其中url的68409293部分即为id，点击跳转后到地址https://www.pixiv.net/member_illust.php?mode=medium&illust_id=68409293，最后跟的就是id。