//[START all]
package com.example.guestbook;

import com.google.appengine.api.datastore.Blob;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;
import com.google.appengine.api.users.User;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import com.google.appengine.api.urlfetch.HTTPHeader;
import com.google.appengine.api.urlfetch.HTTPResponse;
import com.google.appengine.api.urlfetch.URLFetchService;
import com.google.appengine.api.urlfetch.URLFetchServiceFactory;

import java.io.IOException;
import java.util.Date;
import java.net.URL;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class SignGuestbookServlet extends HttpServlet {
  @Override
  public void doPost(HttpServletRequest req, HttpServletResponse resp)
      throws IOException {
    UserService userService = UserServiceFactory.getUserService();
    User user = userService.getCurrentUser();

    Key timelineKey = KeyFactory.createKey("timeline", "timeline_key");
    String content = req.getParameter("content");
    Date date = new Date();
    Entity post = new Entity("post", timelineKey);
    if (user != null) {
        post.setProperty("author", user.getEmail());
    }
    post.setProperty("date", date);
    if (!req.getParameter("url").trim().isEmpty()) {
    	post.setProperty("img", new Blob(fetchImage(req.getParameter("url"))));
    }
    post.setProperty("content", content);

    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
    datastore.put(post);
    
    resp.sendRedirect("/mainpage.jsp");
  }
  
  private byte[] fetchImage(String url){
	  URLFetchService fetchService = URLFetchServiceFactory.getURLFetchService();
      HTTPResponse resp;
      
      try {
	      resp = fetchService.fetch(new URL(url));
      } catch (IOException e) {
          e.printStackTrace();
  	      return null;
      }
 
      return resp.getContent();
  }
}
//[END all]
