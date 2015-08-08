//[START all]
package com.example.guestbook;

import java.io.IOException;
import java.util.Collections;
import java.util.List;

import com.google.appengine.api.datastore.Blob;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.EntityNotFoundException;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.KeyFactory;

import javax.cache.Cache;
import javax.cache.CacheException;
import javax.cache.CacheFactory;
import javax.cache.CacheManager;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class GetImageServlet extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        String strKey = req.getParameter("key");
        byte[] img = null;
        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        
        // Using memcache to retrieve the images
        Cache cache;
        try {
            CacheFactory cacheFactory = CacheManager.getInstance().getCacheFactory();
            cache = cacheFactory.createCache(Collections.emptyMap());
        } catch (CacheException e) {
            cache = null;
        }
        if (cache != null) {
        	if (cache.containsKey(strKey)) {
        		img = (byte[]) cache.get(strKey);
        	}
        }
        
        if (img == null){
        	Entity post;
    		try {
    			post = datastore.get(KeyFactory.stringToKey(strKey));
    			Blob blob = (Blob) post.getProperty("img");
    			img = blob.getBytes();
    			cache.put(strKey, img);
    		} catch (EntityNotFoundException e) {
    			e.printStackTrace();
    		}
        }
        
        resp.setContentType("image/png");
        resp.getOutputStream().write(img);
    }

}