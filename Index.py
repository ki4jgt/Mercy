#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")

from gi.repository import Gtk, WebKit2


#Welcome to Mercy's core file. Everything else is just fun and games. Oh what
#the hell, so is this! :)

class Mercy(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.session = WebKit2
        self.WebContext = self.session.WebContext.new()
        self.session.CookieManager.set_persistent_storage(self.WebContext.get_cookie_manager(), "cookies.txt", self.session.CookiePersistentStorage(0))
        #self.session.CookieManager.connect("changed", self.UpdateCookies)

        #Window details:
        self.set_default_size(200, 200)
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Mercy .:. All you have to do is ask!"
        self.set_titlebar(self.header)

        #Window elements
        self.back_button = Gtk.Button(label = "<", expand = True)
        self.forward_button = Gtk.Button(label = ">", expand = True)
        self.tabs = Gtk.Notebook(scrollable = True, expand = True, tab_pos = 3)
        self.tabs.popup_enable()
        self.abar = Gtk.Entry(expand = True)

        self.pages = []

        #Window Grid
        self.grid = Gtk.Grid()
        self.grid.attach(self.back_button, 0, 0, 1, 100)
        self.grid.attach(self.tabs, 1, 0, 200, 100)
        self.grid.attach(self.forward_button, 201, 0, 1, 100)
        self.grid.attach(self.abar, 1, 100, 200, 1)

        #add grid to window
        self.add(self.grid)

        #Connections:
        self.back_button.connect("clicked", self.GoBack)
        self.forward_button.connect("clicked", self.GoForward)
        self.abar.connect("activate", self.PageLoad)
        self.tabs.connect("switch-page", self.TabChanged)

        self.newTab("http://www.google.com")

    def GoBack(self, Button):
            self.pages[self.tabs.get_current_page()][0].go_back()

    def GoForward(self, Button):
            self.pages[self.tabs.get_current_page()][0].go_forward()

    def PageLoad(self, key):
        if self.abar.get_text() == "NT":
            self.newTab("http://www.google.com")
        elif self.abar.get_text().startswith("ref:"):
            pass
        else:
            if "http" not in self.abar.get_text():
                self.abar.set_text("http://" + self.abar.get_text())
            self.pages[self.tabs.get_current_page()][0].load_uri(self.abar.get_text())

    def URIChanged(self, WebView, WebResource):
        self.abar.set_text(self.pages[self.tabs.get_current_page()][0].get_uri())

    def TabChanged(self, tabs, page, page_num):
        self.abar.set_text(self.pages[page_num][0].get_uri())
        self.forward_button.set_visible(self.pages[page_num][0].can_go_forward())
        self.back_button.set_visible(self.pages[page_num][0].can_go_back())

    def TabRequest(self, webkit, decision, decision_type):
        print(decision)
        print(decision_type)

    def UpdateLoad(self, webview, loadevent):
        self.forward_button.set_visible(self.pages[self.tabs.get_current_page()][0].can_go_forward())
        self.back_button.set_visible(self.pages[self.tabs.get_current_page()][0].can_go_back())

    def UpdateCookies(self):
        self.session.CookieManager.set_persistent_storage(self.WebContext.get_cookie_manager(), "cookies.txt", self.session.CookiePersistentStorage(0))

    def newTab(self, page):
        self.pages.append([self.session.WebView(), Gtk.Label("New Tab")])
        self.pages[-1][0].connect("notify::uri", self.URIChanged)
        self.pages[-1][0].connect("load-changed", self.UpdateLoad)
        self.pages[-1][0].connect("decide-policy", self.TabRequest)
        self.pages[-1][0].load_uri(page)
        self.tabs.insert_page(self.pages[-1][0], self.pages[-1][1], self.tabs.get_n_pages())
        self.tabs.show_all()

main = Mercy()
main.connect("delete-event", Gtk.main_quit)
main.show_all()
Gtk.main()
