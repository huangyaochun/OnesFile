package com.hycjsp.test;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Enumeration;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;

import com.sun.java_cup.internal.runtime.Symbol;

public class FirstFilter implements Filter {
	/**
	 * @see Filter#destroy()
	 */
	public void destroy() {
		// TODO Auto-generated method stub
		this.filterConfig = null;
	}

	/**
	 * @see Filter#doFilter(ServletRequest, ServletResponse, FilterChain)
	 */
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		// TODO Auto-generated method stub
		// place your code here
		System.out.println("begin headers----------------");
		Enumeration headerNames = ((HttpServletRequest)request).getHeaderNames();
		while(headerNames.hasMoreElements()){
			String headerName = (String)headerNames.nextElement();
			System.out.println(headerName + "：" + ((HttpServletRequest)request).getHeader(headerName));
		}
		System.out.println("end headers-------------------");
		
		//在调用目标前写入响应内容
		response.setContentType("text/html;charset=gb2312");
		PrintWriter out = response.getWriter();
		out.println("IP地址为：" + request.getRemoteHost() + "<br>");
		
		// pass the request along the filter chain
/*		chain.doFilter(request, response);
		
		//在目标返回后写入响应内容
		out.println("<br>名称为encoding的初始化参数的值为：" + paramValue);
		out.println("<br>当前Web程序的真实路径为：" + filterConfig.getServletContext().getRealPath("/"));
		//out.println("<br>修改了test.html文件");
*/	
		String docType = "<!DOCTYPE html> \n";
		String title = "道家《清心决》";
		out.println(docType + 
		"<html>\n" +
		"<head><meta charset=\"gb2312\"><title>" + title + "</title></head>\n" + 
		"<body bgcolor=\"#f0f0f0\">\n" + 
		"<h1 align=\"center\">" + title + "</h1>\n" + 
		"<table width=\"30%\" border=\"1\" align=\"center\">\n" );
		String qxj = "心若冰清，天塌不惊，万变犹定，神怡气静，尘垢不沾，俗相不染，虚空宁宓，混然无物，无有相生，难易相成，份与物忘，同乎浑涅，天地无涯，万物齐一，飞花落叶，虚怀若谷，千般烦忧，才下心头，即展眉头，灵台清悠，心无挂碍，意无所执，解心释神，莫然无魂，水流心不惊，云在意俱迟，一心不赘物，古今自逍遥，清心如水，清水即心，微风无起，波澜不惊，幽篁独坐，长啸鸣琴，禅寂入定，毒龙遁形，我心无窍，天道酬勤，我义凛然，鬼魅皆惊，我情豪溢，天地归心，我志扬迈，水起风生！，天高地阔，流水行云，清新治本，直道谋身，至性至善，大道天成！";
		int i = 0;
		for(String aa : qxj.split("，")){
			i+=1;
			if (i == 1){
				out.print("<tr bgcolor=\"#00FA9A\">\n" +
						"<th>"+aa+"</th>");
			}else{
				out.println("<th>"+aa+"</th>\n" + 
				"</tr>\n");
				i = 0;
			}
		}
		
//		out.println("<tr bgcolor=\"#949494\">\n" +
//				"<th>aa</th><th></th>\n" + 
//				"</tr>\n");
		out.println("</table>\n");
		out.println("</body></html>");
	
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	private FilterConfig filterConfig = null;
	String paramValue = null;
	@Override
	public void init(FilterConfig filterConfig) throws ServletException {
		// TODO Auto-generated method stub
		this.filterConfig = filterConfig;
		paramValue = filterConfig.getInitParameter("encoding");
	}

}
