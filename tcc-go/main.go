package hello

import (
    "appengine/user"

	"net/http"
    "io/ioutil"
    "html/template"

    "appengine"
    "appengine/urlfetch"
    "appengine/datastore"

    "time"

    "appengine/memcache"
)

type Post struct {
    Text  string
    Author  string
    Img    []byte
    Date   time.Time
    AuxKey string
}

type HomePageData struct {
    Posts []Post
    User *user.User
    URL     string
}

var(
    timelineKey   *datastore.Key
)

func getTimelineKey(c appengine.Context) *datastore.Key {
    if timelineKey == nil {
        timelineKey = datastore.NewKey(c, "Timeline", "timeline_key", 0, nil)
    }
    return timelineKey
}

func init(){
	http.HandleFunc("/", root)
	http.HandleFunc("/sign", sign)
    http.HandleFunc("/img", serveImage)
}

// Main Page
func root(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    tmpl := template.Must(template.ParseFiles("home.html"))    

	q := datastore.NewQuery("Post").Ancestor(getTimelineKey(c)).Limit(5).Order("-Date")
	var posts []Post
    keys, err := q.GetAll(c, &posts)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

    for i, _ := range posts {
        posts[i].AuxKey = keys[i].Encode()
    }
    
    u := user.Current(c)
    var url string
    if u != nil {
        url, _ = user.LogoutURL(c, "/")
    } else {
        url, _ = user.LoginURL(c, "/")
        http.Redirect(w, r, url, http.StatusSeeOther)
    }
    
    data := &HomePageData {
        Posts : posts,
        User  : u,
        URL   : url,
    }
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := tmpl.Execute(w, data); err != nil {
		c.Errorf("%v", err)
	}
}

func sign(w http.ResponseWriter, r *http.Request) {
    context := appengine.NewContext(r)
    
    // Fetching image
    client := urlfetch.Client(context)    
    fetchResp, fetchErr := client.Get(r.FormValue("url"))
    if fetchErr != nil {
        http.Error(w, fetchErr.Error(), http.StatusInternalServerError)
    }
    bytes, readErr := ioutil.ReadAll(fetchResp.Body) 
    if readErr != nil {
		http.Error(w, readErr.Error(), http.StatusInternalServerError)
	}

    name := user.Current(context).String()
    
    post := &Post{
        Text   : r.FormValue("text"),
        Date   : time.Now(),
        Img    : bytes,
        Author : name,
    }

    postKey := datastore.NewIncompleteKey(context, "Post", getTimelineKey(context))
    _, putErr := datastore.Put(context, postKey, post)
    if putErr != nil {
            http.Error(w, putErr.Error(), http.StatusInternalServerError)
            return
    }
    http.Redirect(w, r, "/", http.StatusSeeOther)
}

func serveImage(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    w.Header().Set("Content-Type", "img/png; charset=utf-8")
    keyStr := r.FormValue("key")
    var img []byte
    
    // Using memcache to retrieve image
    if item, err := memcache.Get(c, keyStr); err == nil{
        img = item.Value
    } else { 
        key, _ := datastore.DecodeKey(keyStr)
        e := new (Post)
        datastore.Get(c, key, e)
        img = e.Img
        
        item = &memcache.Item{
            Key:   keyStr,
            Value: (e.Img),
        }
        memcache.Add(c, item)
    }

    w.Write(img)
}

