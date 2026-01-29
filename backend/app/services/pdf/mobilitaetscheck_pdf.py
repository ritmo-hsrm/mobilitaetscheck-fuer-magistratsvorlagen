from io import BytesIO
from os import path

from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.services.pdf.base_pdf import BasePDF
from app.utils.pdf_util import calculate_average_impact, get_display_impact


class MobilitaetscheckPDF(BasePDF):
    def footer(self):
        self.set_y(-20)
        # self.set_font("free-sans", "", 8)
        # self.cell(
        #     0,
        #     10,
        #     "Hinweis: Die zu den Indiaktoren zugehörigen Dokumente finden Sie alle im Wissensspeicher",
        #     new_x="LMARGIN",
        #     new_y="NEXT",
        # )
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def export(self, eingabe: MobilitaetscheckEingabe):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_font("free-sans", "B", 16)
        self.cell(
            0,
            10,
            "Mobilitätscheck für Magistratsvorlagen",
            border=False,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_font("free-sans", "", 10)

        self.cell(52, 5, txt="**Magistratsvorlagennummer:**", markdown=True)
        self.cell(
            0,
            5,
            txt=f"{eingabe.magistratsvorlage.verwaltungsvorgang_nr}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)
        self.cell(52, 5, txt="**Datum der Magistratssitzung:**", markdown=True)
        self.cell(
            0,
            5,
            txt=f"{eingabe.magistratsvorlage.verwaltungsvorgang_datum.strftime('%d.%m.%Y')}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)
        self.cell(35, 5, txt="**Maßnahme:**", markdown=True)
        self.multi_cell(0, 5, txt=f"{eingabe.name}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.cell(35, 5, txt="**Beschreibung:**", markdown=True)
        self.multi_cell(
            0,
            5,
            txt=f"{eingabe.magistratsvorlage.beschreibung}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        # self.ln(2)
        # self.cell(35, 5, txt="**Sachbearbeitung:**", markdown=True)
        # editors = ""
        # if eingabe.erstellt_von:
        #     editors = f"{eingabe.autor.vorname} {eingabe.autor.nachname}"
        # if eingabe.zuletzt_bearbeitet_von:
        #     if eingabe.erstellt_von != eingabe.zuletzt_bearbeitet_von:
        #         editors += f", {eingabe.letzter_bearbeiter.vorname} {eingabe.letzter_bearbeiter.nachname}"

        # self.cell(0, 5, txt=editors, new_x="LMARGIN", new_y="NEXT")

        self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")

        durchschnitt_auswirkung_oberziel = calculate_average_impact(eingabe)

        box_x = self.get_x()
        box_y = self.get_y()

        self.cell(
            0,
            10,
            "**Zielampel laut verkehrlichem Leitbild**",
            markdown=True,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        script_dir = path.dirname(path.abspath(__file__))
        image_path = path.join(
            script_dir, "./assests/legende.png"
        )  # Navigate to assets
        # Normalize the path for compatibility
        image_path = path.normpath(image_path)
        self.image(image_path, box_x + 115, box_y + 3, 70)
        self.set_font("free-sans", "", 10)

        for oberziel in eingabe.eingabe_ziel_ober:
            display_impact = get_display_impact(
                durchschnitt_auswirkung_oberziel[oberziel.ziel_ober_id],
                oberziel.tangiert,
            )

            # Draw rounded rectangle for background
            current_x = self.get_x()
            current_y = self.get_y()
            cell_height = 8

            self.set_fill_color(
                r=display_impact["color"]["r"],
                g=display_impact["color"]["g"],
                b=display_impact["color"]["b"],
            )
            self.rect(
                current_x, current_y, self.epw, cell_height, style="F", corner_radius=3
            )

            # Place text on top
            self.cell(
                0,
                cell_height,
                txt=f"{oberziel.ziel_ober.nr}. {oberziel.ziel_ober.name}",
                markdown=True,
                fill=False,
                new_y="NExT",
                new_x="LMARGIN",
            )
        box_h = self.get_y() - box_y
        self.rect(box_x, box_y, self.epw, box_h, corner_radius=5)

        # All main objective and only targeted sub objectives are displayed

        self.set_font("free-sans", "", 11)
        self.cell(0, 5, new_x="LMARGIN", new_y="NEXT")

        padding = [0, 10, 0, 0]

        for ix, oberziel in enumerate(eingabe.eingabe_ziel_ober):

            self.set_line_width(0.25)

            self.cell(10, 10, txt=f"**{oberziel.ziel_ober.nr}**", markdown=True)

            self.multi_cell(
                145,
                10,
                txt=f"**{oberziel.ziel_ober.name}**",
                markdown=True,
                max_line_height=5,
                padding=padding,
                new_y="TOP",
            )

            display_impact = get_display_impact(
                durchschnitt_auswirkung_oberziel[oberziel.ziel_ober_id],
                oberziel.tangiert,
            )

            # Draw rounded rectangle for Gesamtwirkung background
            gesamt_x = self.get_x()
            gesamt_y = self.get_y()
            gesamt_width = 35
            gesamt_height = 10

            self.set_fill_color(
                r=display_impact["color"]["r"],
                g=display_impact["color"]["g"],
                b=display_impact["color"]["b"],
            )
            self.rect(
                gesamt_x,
                gesamt_y,
                gesamt_width,
                gesamt_height,
                style="F",
                corner_radius=3,
            )

            # Place text on top
            self.multi_cell(
                gesamt_width,
                gesamt_height,
                txt=f"**Gesamtwirkung:** \n{display_impact["label"]}",
                markdown=True,
                fill=False,
                max_line_height=5,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            self.set_line_width(0.1)

            for index, unterziel in enumerate(oberziel.eingabe_ziel_unter):

                if unterziel.tangiert:
                    if index == 0:
                        self.set_line_width(0.25)
                    else:
                        self.set_line_width(0.1)

                    self.cell(0, 0, border="T", new_x="LMARGIN", new_y="NEXT")

                    self.cell(
                        10,
                        10,
                        txt=f"{oberziel.ziel_ober.nr}.{
                    unterziel.ziel_unter.nr}",
                        markdown=True,
                        border="T",
                    )

                    self.multi_cell(
                        145,
                        10,
                        txt=f"{unterziel.ziel_unter.name}",
                        markdown=True,
                        max_line_height=5,
                        border="T",
                        padding=padding,
                        new_y="TOP",
                    )
                    display_impact = get_display_impact(
                        unterziel.auswirkung, unterziel.tangiert
                    )

                    # Draw rounded rectangle for Wirkung background
                    wirkung_x = self.get_x()
                    wirkung_y = self.get_y()
                    wirkung_width = 35
                    wirkung_height = 10

                    self.set_fill_color(
                        r=display_impact["color"]["r"],
                        g=display_impact["color"]["g"],
                        b=display_impact["color"]["b"],
                    )
                    self.rect(
                        wirkung_x,
                        wirkung_y,
                        wirkung_width,
                        wirkung_height,
                        style="F",
                        corner_radius=3,
                    )

                    # Draw top border
                    self.line(
                        wirkung_x, wirkung_y, wirkung_x + wirkung_width, wirkung_y
                    )

                    # Place text on top
                    self.multi_cell(
                        wirkung_width,
                        wirkung_height,
                        txt=f"**Wirkung:**\n{display_impact["label"]}",
                        markdown=True,
                        border=False,
                        max_line_height=5,
                        fill=False,
                        new_x="LEFT",
                        new_y="NEXT",
                    )

                    raeumlich_name = getattr(
                        unterziel.auswirkung_raeumlich, "name", None
                    )
                    if not raeumlich_name:
                        raeumlich_name = "k/A"
                    self.multi_cell(
                        35,
                        10,
                        txt=f"**Räumlich:**\n{raeumlich_name}",
                        markdown=True,
                        max_line_height=5,
                        new_x="LMARGIN",
                        new_y="TOP",
                    )
                    self.cell(10, 5)
                    # table_x = self.get_x()
                    self.cell(25, 5, txt="**Anmerkung:**", markdown=True)
                    if unterziel.anmerkung:
                        self.multi_cell(
                            120,
                            5,
                            txt=unterziel.anmerkung,
                            padding=padding,
                            new_x="LMARGIN",
                            new_y="NEXT",
                        )
                        self.cell(145, 1, new_x="LMARGIN", new_y="NEXT")

                    else:
                        self.cell(0, 5, txt="-", new_x="LMARGIN", new_y="NEXT")

                    self.cell(10, 5)
                    # self.cell(25,5, txt="**Indikatoren:**", markdown=True)
                    # self.multi_cell(120,5, txt=', '.join(indicator.label for indicator in sub_objective.indicators), markdown=True, padding=padding, new_x="LMARGIN", new_y="NEXT")
                    # Set the label for "Indikatoren:"
                    self.cell(25, 5, txt="**Indikatoren:**", markdown=True)
                    if unterziel.indikatoren:

                        # Fixed indentation for bullet points
                        bullet_indent = (
                            45  # Adjust this value to align with "Indikatoren:"
                        )

                        # Start adding indicators as a bulleted list on the same line
                        for i, indikator in enumerate(unterziel.indikatoren):
                            # Set the x position for bullet points alignment
                            self.set_x(bullet_indent)

                            # Set bullet point and label text
                            bullet_point = "• "
                            label_text = bullet_point + indikator.name

                            # Add hyperlink if a source URL exists, otherwise just add text
                            if indikator.quelle_url:
                                self.set_text_color(
                                    0, 0, 255
                                )  # Optional: set link color to blue
                                self.cell(
                                    0, 5, label_text, link=indikator.quelle_url, ln=1
                                )
                                self.set_text_color(
                                    0, 0, 0
                                )  # Reset color after the link text
                            else:
                                self.cell(0, 5, label_text, ln=1)
                    else:
                        self.cell(
                            0, 5, txt="-", markdown=True, new_x="LMARGIN", new_y="NEXT"
                        )

            if not ix == len(eingabe.eingabe_ziel_ober) - 1:
                self.set_line_width(0.5)
                self.cell(0, 1, border="B", new_x="LMARGIN", new_y="NEXT")
                self.cell(0, 1, new_x="LMARGIN", new_y="NEXT")
        # Create a bytes buffer to save the self
        pdf_output = BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output
