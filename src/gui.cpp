#include "gui.h"
#include <iostream>

GUI::GUI() {
    app = gtk_application_new("com.openwire.main", G_APPLICATION_FLAGS_NONE);
    adapterCombo = nullptr;
    processListBox = nullptr;
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

void GUI::setProcesses(const std::vector<processInfo>& processes) {
    this->processes = processes;
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

void GUI::createProcessSidebar(GtkWidget *parent) {
    GtkWidget *scrolled = gtk_scrolled_window_new();
    gtk_widget_set_size_request(scrolled, 300, -1);

    processListBox = GTK_LIST_BOX(gtk_list_box_new());
    gtk_list_box_set_selection_mode(processListBox, GTK_SELECTION_SINGLE);
    g_signal_connect(processListBox, "row-selected", G_CALLBACK(GUI::onProcessRowSelected), this);

    // Add an 'All' option as the first selectable item
    {
        const char* allLabel = "All (99999)";
        GtkWidget *rowChild = gtk_label_new(allLabel);
        gtk_widget_set_halign(rowChild, GTK_ALIGN_START);
        gtk_list_box_append(processListBox, rowChild);
    }

    // Populate list with process names
    for (const auto& p : processes) {
        std::string labelText = p.processName + " (" + std::to_string(p.pid) + ")";
        GtkWidget *rowChild = gtk_label_new(labelText.c_str());
        gtk_widget_set_halign(rowChild, GTK_ALIGN_START);
        gtk_list_box_append(processListBox, rowChild);
    }

    gtk_scrolled_window_set_child(GTK_SCROLLED_WINDOW(scrolled), GTK_WIDGET(processListBox));
    gtk_box_append(GTK_BOX(parent), scrolled);
}

void GUI::onAdapterChanged(GtkComboBoxText *combo, gpointer user_data) {
    GUI* gui = static_cast<GUI*>(user_data);
    gchar *selected = gtk_combo_box_text_get_active_text(combo);
    if (selected) {
        std::cout << "Selected adapter: " << selected << std::endl;
        g_free(selected);
    }
}

void GUI::onProcessRowSelected(GtkListBox *box, GtkListBoxRow *row, gpointer user_data) {
    if (!row) return; // deselection
    GUI* gui = static_cast<GUI*>(user_data);
    int index = gtk_list_box_row_get_index(row);
    // index 0 is the 'All' row; real processes start at 1
    if (index == 0) {
        std::cout << "Selected PID: 99999" << std::endl;
        return;
    }
    size_t procIdx = static_cast<size_t>(index - 1);
    if (procIdx < gui->processes.size()) {
        const auto& p = gui->processes[procIdx];
        std::cout << "Selected PID: " << p.pid << std::endl;
    }
}

void GUI::activate(GtkApplication* app, gpointer user_data) {
    GUI* gui = static_cast<GUI*>(user_data);
    
    GtkWidget *window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "OpenWire");
    gtk_window_set_default_size(GTK_WINDOW(window), 1280, 720);

    // Root horizontal layout: [Sidebar | Content]
    GtkWidget *root = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    gtk_widget_set_margin_top(root, 10);
    gtk_widget_set_margin_bottom(root, 10);
    gtk_widget_set_margin_start(root, 10);
    gtk_widget_set_margin_end(root, 10);
    gtk_window_set_child(GTK_WINDOW(window), root);

    // Left: process sidebar
    gui->createProcessSidebar(root);

    // Right: content container (reuse existing adapter dropdown)
    GtkWidget *content = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_box_append(GTK_BOX(root), content);
    gui->createDropdownMenu(content);

    gtk_widget_show(window);
}
