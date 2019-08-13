package com.hycjsp.test;

import java.util.*;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

//实现Filter类
public class LogFilter implements Filter {
	public void init(FilterConfig config) throws ServletException {
		// 获取初始化参数
		String site = config.getInitParameter("Site");
		// 输出初始化参数
		System.out.println("网站名称：" + site);
		
	}
	
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
			throws java.io.IOException, ServletException {
		// 输出站点名称
		System.out.println("站点网址：http://www.runoob.com");
		// 把请求传回过滤链
		chain.doFilter(request, response);
	}

	public void destroy() {
		/* 在Filter实例被Web容器从服务器移除之前调用 */
	}
}
