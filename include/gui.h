#ifndef GUI_H
#define GUI_H
#include <gtk/gtk.h>
#include "adapters.h"
#include <vector>

class GUI {
    public:
        GUI();
        ~GUI();

        void run();
        void setAdapters(const std::vector<NetworkAdapter>& adapters);
    private:
        GtkApplication *app;
        std::vector<NetworkAdapter> adapters;
        GtkComboBoxText *adapterCombo;
        
        void createDropdownMenu(GtkWidget *container);
        static void activate(GtkApplication* app, gpointer user_data);
        static void onAdapterChanged(GtkComboBoxText *combo, gpointer user_data);
};
#endif 