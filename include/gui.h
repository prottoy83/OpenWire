#ifndef GUI_H
#define GUI_H
#include <gtk/gtk.h>
#include "adapters.h"
#include "process.h"
#include <vector>

class GUI {
    public:
        GUI();
        ~GUI();

        void run();
        void setAdapters(const std::vector<NetworkAdapter>& adapters);
        void setProcesses(const std::vector<processInfo>& processes);
    private:
        GtkApplication *app;
        std::vector<NetworkAdapter> adapters;
        GtkComboBoxText *adapterCombo;
        std::vector<processInfo> processes;
        GtkListBox* processListBox;
        
        void createDropdownMenu(GtkWidget *container);
        void createProcessSidebar(GtkWidget *parent);
        static void activate(GtkApplication* app, gpointer user_data);
        static void onAdapterChanged(GtkComboBoxText *combo, gpointer user_data);
        static void onProcessRowSelected(GtkListBox *box, GtkListBoxRow *row, gpointer user_data);
};
#endif 