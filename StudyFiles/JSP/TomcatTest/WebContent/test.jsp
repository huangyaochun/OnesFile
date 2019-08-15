<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="java.io.*,java.util.*,java.text.*"  %>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>学习JSP</title>
</head>
<body>

<%! int day = 6; %> <!-- 声明变量 -->

<p>
今天的日期是：
<%= (new java.util.Date()).toLocaleString() %> <!-- 表达式2 -->
</p>
<%
out.println("hello World!!<br/>");
out.println("Your IP address is " + request.getRemoteAddr()+"<br/>");
out.println("你的IP地址是： " + request.getRemoteAddr());
%>

<h3>SWITCH...CASE 实例</h3>
<%
switch(day){
case 0:
	out.println("星期天");
	break;
case 1:
	out.println("星期一");
	break;
case 2:
	out.println("星期二");
	break;
case 3:
    out.println("星期三");
    break;
case 4:
    out.println("星期四");
    break;
case 5:
    out.println("星期五");
    break;
case 6:
    out.println("星期六");
    break;
}
%>

 <h1>While 循环实例</h1>
 <%! int fontSize = 2; %>
 <%while(fontSize<=7){ %>
     fontSize =<%= fontSize %>
    <font color="green" size=<%= fontSize %>>Yes,I'm Good!</font><br/>
 <%fontSize++; %>
<%} %>


<h6>For 循环实例</h6>
fontSize =<%= fontSize %><br>
<%for(fontSize = 7; fontSize>=2;fontSize--){ %>
	fontSize =<%= fontSize %>
    <font color="red" size="<%= fontSize %>">
         我最强大！
    </font><br/>
 <%} %>


<h2>include 动作实例</h2>
<jsp:include page="TestLife.jsp" flush="false" /> <!--JSP动作元素 插入TestLife.jsp 页面 ，相当于另一个页面-->

<h2>Include 指令</h2>
<%@include file="TestLife.jsp"%> <!--Include指令添加TestLife.jsp 页面 ，相当于当前页面-->
 
 <h2>Jsp 使用 JavaBean 实例</h2>
 <jsp:useBean id="test" class="com.hycjsp.main.TestBean"></jsp:useBean>
 <jsp:setProperty property="message" name="test" value = "cai鸟一枚。。。"/> 
 <p>输出信息....</p>
 <jsp:getProperty property="message" name="test"/>
 
 <%--<h2>forward 动作实例</h2>
 <jsp:forward page="TestLife.jsp"></jsp:forward> --%>

    <jsp:element name="xmlElement">
    <jsp:attribute name="xmlElementAttr">
       属性值
    </jsp:attribute>
    <jsp:body>
       XML 元素的主体
    </jsp:body>
    </jsp:element>
    
<books><book><jsp:text>  
    Welcome to JSP Programming
</jsp:text></book></books>

<h2>HTTP 头部请求实例</h2>

<table width="100%" border="1" align="center">
<tr bgcolor="#949494">
<th>Header Name</th>
<th>Header Value(s)</th>
</tr>
<%
out.println("端口号port:" + request.getServerPort());
out.println("刷新:" + request.getIntHeader("Refresh"));
Enumeration headerNames = request.getHeaderNames();
while(headerNames.hasMoreElements()){
	String paramName = (String)headerNames.nextElement();
	out.println("<tr><td>" + paramName + "</td>\n");
	String paramValue = request.getHeader(paramName);
	out.println("<td>" + paramValue + "</td></tr>\n");
}
%>
</table>

<h2>自动刷新实例</h2>
<%
//设置每隔5s自动刷新
response.setIntHeader("Refresh", 10);
//获取当前时间
Calendar calendar = new GregorianCalendar();
String am_pm;
SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.CHINA);
int hour = calendar.get(Calendar.HOUR);
int minute = calendar.get(Calendar.MINUTE);
int second = calendar.get(Calendar.SECOND);
if(calendar.get(Calendar.AM_PM) == 0)
	am_pm = "AM";
else
	am_pm = "PM";
String CT = hour+":"+minute+":"+second+" "+am_pm;
out.println("当前时间：" + CT + "\n" + "具体时间：" + format.format(calendar.getTime()) + "\n");
response.reset();
response.setCharacterEncoding("UTF-8");
%>

<%
   // 设置错误代码，并说明原因
   // response.sendError(407, "Need authentication!!!" );
%>
<br>

<h2>使用 POST</h2>
<form action="main.jsp" method="POST">
站点名: <input type="text" name="name">
<br />
网址: <input type="text" name="url" />
<input type="submit" value="提交" />
</form>

<h1>使用 GET 方法读取数据</h1>
<ul>
<li><p>
<b>站点名：</b>
<%= request.getParameter("name") %>
</p></li>
<li><p>
<b>网址：</b>
<%= request.getParameter("url") %>
</p></li>
</ul>

<h1>从复选框中读取数据</h1>
<ul>
<li><p><b>Google 是否选中：</b><%=request.getParameter("google") %></p></li>
<li><p><b>百度  是否选中：</b><%=request.getParameter("baidu") %></p></li>
<li><p><b>淘宝  是否选中：</b><%=request.getParameter("taobao") %></p></li>
</ul>

<h1>读取所有表单参数</h1>
<table width="100%" border="1" align="center">
<tr bgcolor="#949494">
<th>参数名</th><th>参数值</th>
</tr>
<%
 Enumeration paramNames = request.getParameterNames();
 while(paramNames.hasMoreElements()){
	 String paramName = (String)paramNames.nextElement();
	 out.print("<tr><td>" + paramName +"</td>\n");
	 String paramValue = request.getParameter(paramName) ;
	 out.println("<td>" + paramValue + "</td></tr>\n");
 }
%>
</table>

<%
//获取session创建时间
Date createTime = new Date(session.getCreationTime());
//获取最后访问页面的时间
Date lastAccessTime = new Date(session.getLastAccessedTime());

String title = "再次访问session教程实例";
Integer visitCount = new Integer(0);
String visitCountKey = new String("visitCount");
String userIDKey = new String("userID");
String userID = new String("ABCD");

//检测网页是否有新的访问用户
if(session.isNew()){
	title = "访问session教程实例";
	//使用指定的名称和值来产生一个对象并绑定到session中
	session.setAttribute(userIDKey, userID); 
	session.setAttribute(visitCountKey, visitCount);
}else{
	//返回session对象中与指定名称绑定的对象，如果不存在则返回null
	visitCount = (Integer)session.getAttribute(visitCountKey);
	visitCount += 1;
	userID = (String)session.getAttribute(userIDKey);
	session.setAttribute(visitCountKey, visitCount);
}
%>

<h1>Session 跟踪</h1>
<table border="1" align="center">
<tr bgcolor="#949494">
	<th>Session 信息</th>
	<th>值</th>
</tr>
<tr>
	<td>id</td>
	<td><%out.print(session.getId()); %></td>
</tr>
<tr>
	<td>创建时间</td>
	<td><%out.print(createTime); %></td>
</tr>
<tr>
	<td>最后访问时间</td>
	<td><%out.print(lastAccessTime); %></td>
</tr>
<tr>
	<td>用户ID</td>
	<td><%out.print(userID); %></td>
</tr>
<tr>
	<td>访问次数</td>
	<td><%out.print(visitCount); %></td>
</tr>
</table>

</body>
</html>