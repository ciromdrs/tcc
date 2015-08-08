<%-- //[START all]--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.google.appengine.api.users.User" %>
<%@ page import="com.google.appengine.api.users.UserService" %>
<%@ page import="com.google.appengine.api.users.UserServiceFactory" %>
<%-- //[START imports]--%>
<%@ page import="com.google.appengine.api.datastore.Blob" %>
<%@ page import="com.google.appengine.api.datastore.DatastoreService" %>
<%@ page import="com.google.appengine.api.datastore.KeyFactory" %>
<%@ page import="com.google.appengine.api.datastore.DatastoreServiceFactory" %>
<%@ page import="com.google.appengine.api.datastore.Entity" %>
<%@ page import="com.google.appengine.api.datastore.FetchOptions" %>
<%@ page import="com.google.appengine.api.datastore.Key" %>
<%@ page import="com.google.appengine.api.datastore.KeyFactory" %>
<%@ page import="com.google.appengine.api.datastore.Query" %>
<%-- //[END imports]--%>
<%@ page import="java.util.List" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

<html>
<head>
    <title>Java App</title>
    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css"/>
</head>

<body>

<%
    UserService userService = UserServiceFactory.getUserService();
    User user = userService.getCurrentUser();
    if (user != null) {
        pageContext.setAttribute("user", user);
%>

<p>Hello, ${fn:escapeXml(user.nickname)}! (You can
    <a href="<%= userService.createLogoutURL(request.getRequestURI()) %>">sign out</a>.)</p>
<%
    } else {
        String url = userService.createLoginURL(request.getRequestURI());
        response.sendRedirect(url);
    }
%>

<%-- //[START datastore]--%>
<%
    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
    Key timelineKey = KeyFactory.createKey("timeline", "timeline_key");
    Query query = new Query("post", timelineKey).addSort("date", Query.SortDirection.DESCENDING);
    List<Entity> posts = datastore.prepare(query).asList(FetchOptions.Builder.withLimit(5));
    if (!posts.isEmpty()) {
%>
<%
        for (Entity p : posts) {
            pageContext.setAttribute("content",
                    p.getProperty("content"));
            String author = (String) p.getProperty("author");
            
            pageContext.setAttribute("user", author);
            
            pageContext.setAttribute("key", KeyFactory.keyToString(p.getKey()));
%>
<p><b>${fn:escapeXml(user)}</b> wrote:</p>
<blockquote>${fn:escapeXml(content)}</blockquote>
<%
            if (p.getProperty("img") != null) {
%>
<img src="/img?key=${fn:escapeXml(key)}">
<%
            }
        }
    }
%>

<form action="/sign" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input name="url" type="text" placeholder="Paste a link to an image..."/></div>
    <div><input type="submit"/></div>
</form>
<%-- //[END datastore]--%>

</body>
</html>
<%-- //[END all]--%>
