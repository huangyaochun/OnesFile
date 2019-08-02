<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*" %>    
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
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



</body>
</html>