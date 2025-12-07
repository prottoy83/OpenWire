#include "gui.h"
#include <iostream>

GUI::GUI() {
    app = gtk_application_new("com.openwire.main", G_APPLICATION_FLAGS_NONE);
    adapterCombo = nullptr;
    g_signal_connect(app, "activate", G_CALLBACK(GUI::activate), this);
}

GUI::~GUI() {
    g_object_unref(app);
}

void GUI::run() {
    int status = g_application_run(G_APPLICATION(app), 0, nullptr);
    std::cout << "Application exited with status: " << status << std::endl;
}

void GUI::setAdapters(const std::vector<NetworkAdapter>& adapters) {
    this->adapters = adapters;
}

void GUI::createDropdownMenu(GtkWidget *container) {
    // Create label
    GtkWidget *label = gtk_label_new("Select Network Adapter:");
    gtk_box_append(GTK_BOX(container), label);
    
    // Create dropdown
    adapterCombo = GTK_COMBO_BOX_TEXT(gtk_combo_box_text_new());
    g_signal_connect(adapterCombo, "changed", G_CALLBACK(GUI::onAdapterChanged), this);
    
    // Populate dropdown with adapters
    for (const auto& adapter : adapters) {
        std::string displayText = adapter.description + " (" + adapter.ipAddress + ")";
        gtk_combo_box_text_append(adapterCombo, adapter.name.c_str(), displayText.c_str());
    }
    
    // Set first item as active
    if (!adapters.empty()) {
        gtk_combo_box_set_active(GTK_COMBO_BOX(adapterCombo), 0);
    }
    
    gtk_box_append(GTK_BOX(container), GTK_WIDGET(adapterCombo));
}

void GUI::onAdapterChanged(GtkComboBoxText *combo, gpointer user_data) {
    GUI* gui = static_cast<GUI*>(user_data);
    gchar *selected = gtk_combo_box_text_get_active_text(combo);
    if (selected) {
        std::cout << "Selected adapter: " << selected << std::endl;
        g_free(selected);
    }
}

void GUI::activate(GtkApplication* app, gpointer user_data) {
    GUI* gui = static_cast<GUI*>(user_data);
    
    GtkWidget *window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "OpenWire");
    gtk_window_set_default_size(GTK_WINDOW(window), 1280, 720);
    
    // Create main container
    GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_margin_top(box, 10);
    gtk_widget_set_margin_bottom(box, 10);
    gtk_widget_set_margin_start(box, 10);
    gtk_widget_set_margin_end(box, 10);
    gtk_window_set_child(GTK_WINDOW(window), box);
    
    // Create dropdown menu
    gui->createDropdownMenu(box);
    
    gtk_widget_show(window);
}
