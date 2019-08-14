<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*,java.net.*" %>    
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<% 
//编码，解决中文乱码
String str = URLEncoder.encode(request.getParameter("name"),"utf-8");
//设置name 和 url cookie
Cookie name2 = new Cookie("name",str);
Cookie url = new Cookie("url",request.getParameter("url"));

//设置cookie过期时间为 24小时 = 60*60*24
name2.setMaxAge(10);
url.setMaxAge(10);

// 在响应头部添加cookie
response.addCookie(name2);
response.addCookie( url );
%>


<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Test_Main</title>
</head>
<body>

<h1>使用表单的 GET 方法实例</h1>
<form action = "test.jsp" method="get">
站点名：<input type="text" name="name"><br />
网址：<input type="text" name="url" />
<input type="submit" value="提交" />
</form>

<h1>使用 POST 方法读取数据</h1>
<ul>
<li><p><b>站点名称：</b>
<%
//解决中文乱码问题
String name = new String((request.getParameter("name")).getBytes("ISO-8859-1"),"UTF-8");
%>
<%=name %>
</p></li>
<li><p><b>网址：</b>
<%=request.getParameter("url") %>
</p></li>
</ul>

<h1>设置 Cookie</h1>


<ul>
<li><p><b>coock网站名:</b>
	<%= request.getParameter("name") %>
</p></li>
<li><p><b>coock网址:</b>
	<%= request.getParameter("url") %>
</p></li>
</ul>

</body>
</html>