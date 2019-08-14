<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.net.*" %>
<!DOCTYPE html>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<title>获取 Cookie</title>
</head>
<body>
<%
//编码，解决中文乱码
String str = URLEncoder.encode("神马百度","utf-8");
//设置name 和 url cookie
Cookie cookie = new Cookie("name",str);
//设置cookie过期时间为 24小时 = 60*60*24
cookie.setMaxAge(30);
response.addCookie(cookie);
cookie = new Cookie("url","www.shenmaBaidu.com");
cookie.setMaxAge(30);
response.addCookie(cookie);

//Cookie cookie = null;
Cookie[] cookies = null;
//获取 cookies 的数据，是一个数组
cookies = request.getCookies();
if(cookies != null){
	out.println("<h2>查找Cookie名与值</h2>");
	for(int i = 0;i < cookies.length;i++){
		cookie = cookies[i];
		if((cookie.getName()).compareTo("name")== 0){
			cookie.setMaxAge(0);
			response.addCookie(cookie);
			out.print("删除Cookie:" + cookie.getName() + "<br/>");
		}else{
			out.println("参数名：" + cookie.getName());
			out.print("<br>");
			out.print("参数值：" + URLDecoder.decode(cookie.getValue(),"UTF-8") + "<br>");
			out.print("------------------------------------<br>");
		}

	}
}else{
	out.println("<h2>没有发现Cookie</h2>");
}
%>
</body>

</html>