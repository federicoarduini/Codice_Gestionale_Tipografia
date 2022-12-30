from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QDialog
from ECommerce.Catalogo import Catalogo
import view.AggiungiProdottoView as APV
import view.ModificaProdottoView as MPV


class GestioneProdottiView(QMainWindow):
    def __init__(self):
        super(GestioneProdottiView, self).__init__()

        uic.loadUi('ui/gestione_prodotti.ui', self)
        self.selected_prod_id = None

        self.table_prodotti.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_prodotti.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_add_prod.clicked.connect(self.aggiungi_prodotto)
        self.btn_delete_selected.clicked.connect(self.rimuovi_prodotto)
        self.btn_edit_selected.clicked.connect(self.modifica_prodotto)

        self.catalogo = Catalogo()
        lista_prodotti = self.catalogo.get_lista_prodotti()
        self.carica_catalogo(lista_prodotti)

    def carica_catalogo(self, lista_prodotti):
        # pulizia tabella (per aggiornamenti, ad esempio)
        self.table_prodotti.setRowCount(0)
        # ottengo il numero di righe che vanno inserite
        self.table_prodotti.setRowCount(len(lista_prodotti))
        # inserisco effettivamente le righe
        num_riga = 0
        for prod in lista_prodotti:
            # gli item della qtablewidget devono essere obbligatoriamente delle stringhe, quindi vado a castare
            # i valori numerici in stringhe per renderli visibili in tabella
            prod_id = QTableWidgetItem(str(prod.get_id()))
            prod_title = QTableWidgetItem(prod.get_titolo())
            prod_qta = QTableWidgetItem(str(prod.get_quantita()))
            prod_price = QTableWidgetItem(str(prod.get_prezzo()) + "€")
            prod_descr = QTableWidgetItem(prod.get_descrizione())

            self.table_prodotti.setItem(num_riga, 0, prod_id)
            self.table_prodotti.setItem(num_riga, 1, prod_title)
            self.table_prodotti.setItem(num_riga, 2, prod_qta)
            self.table_prodotti.setItem(num_riga, 3, prod_price)
            self.table_prodotti.setItem(num_riga, 4, prod_descr)

            num_riga += 1

    def aggiungi_prodotto(self):
        aggiunta_prodotto = APV.AggiungiProdottoView(self.catalogo)
        if aggiunta_prodotto.exec():
            self.catalogo = Catalogo()
            self.carica_catalogo(self.catalogo.get_lista_prodotti())

    def rimuovi_prodotto(self):
        prod = list(map(lambda x: int(x.data(0)), self.table_prodotti.selectionModel().selectedRows()))
        for i in prod:
            self.catalogo.db_con.rimuovi_prodotto(i)
        self.catalogo = Catalogo()
        self.carica_catalogo(self.catalogo.get_lista_prodotti())

    def modifica_prodotto(self):
        prod_list = map(lambda x: self.catalogo.ricerca_per_id(int(x.data(0))), self.table_prodotti.selectionModel().selectedRows())
        for prod in prod_list:
            mod_prodotto = MPV.ModificaProdottoView(self.catalogo, prod)
            if mod_prodotto.exec():
                print("prodotto aggiornato")
                self.catalogo = Catalogo()
                self.carica_catalogo(self.catalogo.get_lista_prodotti())
            else:
                print("aggiornamento annullato")
