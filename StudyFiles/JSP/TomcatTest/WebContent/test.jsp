<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
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

</body>
</html>