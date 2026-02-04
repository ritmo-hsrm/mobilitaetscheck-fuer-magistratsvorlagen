from io import BytesIO

from app.models.klimarelevanzpruefung_eingabe import KlimarelevanzpruefungEingabe
from app.services.pdf.base_pdf import BasePDF


class KlimarelevanzpruefungPDF(BasePDF):

    def footer(self):
        self.set_y(-20)
        self.set_font("free-sans", "", 8)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def _add_table_header(self):
        """Add table header with column titles"""
        self.set_font("free-sans", "B", 10)
        num_col_width = 10
        content_col_width = (self.w - 20 - num_col_width) / 2
        self.cell(num_col_width, 8, "Nr.", border=1, align="C")
        self.cell(content_col_width, 8, "Positive Klimaauswirkung", border=1, align="C")
        self.cell(
            content_col_width,
            8,
            "Negative Klimaauswirkung",
            border=1,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

    def _add_table_row(
        self,
        row_num: int,
        positive_text: str = "",
        negative_text: str = "",
        draw_top_border: bool = False,
        show_number: bool = True,
    ):
        """Add a row with numbering in first column, positive and negative in separate columns"""
        num_col_width = 10
        content_col_width = (self.w - 20 - num_col_width) / 2

        # Calculate height needed
        self.set_font("free-sans", "", 9)
        positive_lines = self.multi_cell(
            content_col_width, 5, positive_text, border=0, split_only=True
        )
        negative_lines = self.multi_cell(
            content_col_width, 5, negative_text, border=0, split_only=True
        )
        max_lines = max(len(positive_lines), len(negative_lines), 1)
        row_height = max_lines * 5 + 2

        # Check if we need a new page
        if self.get_y() + row_height > self.h - 25:
            self.add_page()
            self._add_table_header()

        y_start = self.get_y()

        # Set consistent line width for all borders
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)

        # Column positions
        x_num = self.l_margin
        x_pos = self.l_margin + num_col_width
        x_neg = self.l_margin + num_col_width + content_col_width
        x_end = self.l_margin + num_col_width + 2 * content_col_width

        # Draw positive column text first to determine height
        self.set_font("free-sans", "", 9)
        self.set_xy(x_pos, y_start)
        self.multi_cell(content_col_width, 5, positive_text, border=0, align="L")
        y_after_positive = self.get_y()

        # Draw negative column text
        self.set_xy(x_neg, y_start)
        self.multi_cell(content_col_width, 5, negative_text, border=0, align="L")
        y_after_negative = self.get_y()

        # Calculate actual row height
        actual_height = max(y_after_positive, y_after_negative) - y_start
        y_end = y_start + actual_height

        # Draw borders manually for consistent thickness
        # Top border (only if new group - to separate from previous group)
        if draw_top_border:
            self.line(x_num, y_start, x_end, y_start)

        # NO bottom border here - will be drawn at end of table
        # This way rows in the same group have no horizontal line between them

        # Left border (outer)
        self.line(x_num, y_start, x_num, y_end)

        # Right border (outer)
        self.line(x_end, y_start, x_end, y_end)

        # Vertical line after number column
        self.line(x_pos, y_start, x_pos, y_end)

        # Vertical line between positive and negative columns
        self.line(x_neg, y_start, x_neg, y_end)

        # Move to next row
        self.set_y(y_end)

        # Return info for group number positioning
        return y_start, y_end, row_num if show_number else None

    def _draw_group_number(
        self, group_num: int, y_start: float, y_end: float, num_col_width: float
    ):
        """Draw the group number vertically centered within the group's total height"""
        # Save current position
        current_y = self.get_y()

        self.set_font("free-sans", "", 9)
        text_height = 5
        group_height = y_end - y_start
        y_centered = y_start + (group_height - text_height) / 2
        self.set_xy(self.l_margin, y_centered)
        self.cell(num_col_width, text_height, str(group_num), border=0, align="C")

        # Restore position for next row
        self.set_y(current_y)

    def _collect_all_rows(self, eingabe: KlimarelevanzpruefungEingabe):
        """Collect all rows from all questionnaires with group info"""
        rows = []  # List of (group, positive_text, negative_text)

        # FB1 - Fragebogen A
        fb1 = eingabe.fb1 if eingabe.f1 else None
        if fb1:
            # a1: Maschinen/Materialien
            if fb1.a1q1 == 1 and fb1.a1q2:
                rows.append(
                    (
                        "a1",
                        "",
                        f"Im Rahmen des Vorhabens werde(n) {fb1.a1q2} angeschafft.",
                    )
                )

            if fb1.a1q3 == 1:
                rows.append(
                    (
                        "a1",
                        f"Bei der Anschaffung wurde auf Nachhaltigkeitskriterien geachtet. Erläuterung: {fb1.a1q4 or ''}",
                        "",
                    )
                )
            elif fb1.a1q3 == 2:
                rows.append(
                    (
                        "a1",
                        "",
                        f"Bei der Auswahl wurde nicht auf Nachhaltigkeitskriterien geachtet, weil {fb1.a1q5 or ''}",
                    )
                )

            # a2: Energetische Aufwertung / Baumaßnahmen
            if fb1.a2q2 in [3, 4]:
                if fb1.a2q3:
                    rows.append(
                        (
                            "a2",
                            "Bei dem Vorhaben wird ein bestehendes Gebäude energetisch aufgewertet.",
                            "",
                        )
                    )
                    if fb1.a2q4:
                        rows.append(
                            (
                                "a2",
                                f"Dabei wird der Energiestandard {fb1.a2q4_item.name} erreicht. Es wurde sich für den genannten Standard entschieden, da {fb1.a2q5 or ''}",
                                "",
                            )
                        )
            if fb1.a2q2 in [1, 2]:
                if fb1.a2q6 == 6:
                    rows.append(
                        (
                            "a2",
                            "",
                            f"Es wird lediglich der Energiestandard {fb1.a2q6_item.name} erreicht und damit das gesetzliche Mindestmaß erfüllt. Es wurde sich für den genannten Standard entschieden, da {fb1.a2q7 or ''}",
                        )
                    )
                elif fb1.a2q6:
                    rows.append(
                        (
                            "a2",
                            f"Es wird der Energiestandard {fb1.a2q6_item.name} erreicht. Es wurde sich für den genannten Standard entschieden, da {fb1.a2q7 or ''}",
                            "",
                        )
                    )

            if fb1.a2q8 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben wird darauf geachtet, dass Niederschlag möglichst vor Ort versickert.",
                        "",
                    )
                )
            elif fb1.a2q8 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben wird nicht darauf geachtet, dass Niederschlag möglichst vor Ort versickert. Erläuterung: {fb1.a2q9 or ''}",
                    )
                )

            if fb1.a2q10 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben wird darauf geachtet, dass Kaltluftströme ungehindert fließen können.",
                        "",
                    )
                )
            elif fb1.a2q10 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben wird nicht darauf geachtet, dass Kaltluftströme ungehindert fließen können. Erläuterung: {fb1.a2q11 or ''}",
                    )
                )

            if fb1.a2q12 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben finden Maßnahmen gegen die örtliche Hitzebildung Anwendung.",
                        "",
                    )
                )
            elif fb1.a2q12 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben finden keine Maßnahmen gegen die örtliche Hitzebildung Anwendung. Erläuterung: {fb1.a2q13 or ''}",
                    )
                )

            if fb1.a2q14 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei den Vergabekriterien wurde auf Nachhaltigkeit geachtet.",
                        "",
                    )
                )
            elif fb1.a2q14 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei den Vergabekriterien wurde nicht auf Nachhaltigkeit geachtet, weil {fb1.a2q15 or ''}",
                    )
                )

            # a3: Flächenversiegelung
            if fb1.a3q1 == 1:
                neg_text = f"Bei dem Vorhaben werden Flächen im Umfang von {fb1.a3q2 or '?'} m² neu versiegelt."
                if fb1.a3q3:
                    neg_text += f" Bisher wurde die Fläche als {fb1.a3q3} genutzt."
                rows.append(("a3", "", neg_text))

                if fb1.a3q4 == 1:
                    rows.append(
                        (
                            "a3",
                            f"Für die Versiegelung sind Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a3q5 or ''}",
                            "",
                        )
                    )
                elif fb1.a3q4 == 2:
                    rows.append(
                        (
                            "a3",
                            "",
                            f"Für die Versiegelung sind keine Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a3q6 or ''}",
                        )
                    )

            # a4: Flächenentsiegelung
            if fb1.a4q1 == 1:
                pos_text = f"Bei dem Vorhaben werden Flächen im Umfang von {fb1.a4q2 or '?'} m² entsiegelt."
                if fb1.a4q3:
                    pos_text += f" Bisher wurde die Fläche als {fb1.a4q3} genutzt."
                rows.append(("a4", pos_text, ""))

                if fb1.a4q4 == 1:
                    rows.append(
                        (
                            "a4",
                            "",
                            "Die Entsiegelung ist Teil einer Ausgleichsmaßnahme.",
                        )
                    )

            # a5: Grünflächen
            if fb1.a5q1 == 1:
                pos_text = f"Bei dem Vorhaben werden Grünflächen im Umfang von {fb1.a5q2 or '?'} aufgewertet."
                if fb1.a5q3:
                    pos_text += f" Bisher wurde die Fläche als {fb1.a5q3} genutzt."
                rows.append(("a5", pos_text, ""))

                if fb1.a5q4 == 1:
                    rows.append(
                        ("a5", "", "Die Aufwertung ist Teil einer Ausgleichsmaßnahme.")
                    )

            # a6: Begrünung entfernt
            if fb1.a6q1 == 1:
                rows.append(
                    (
                        "a6",
                        "",
                        f"Bei dem Vorhaben wird Begrünung im Umfang von {fb1.a6q2 or '?'} m² entfernt.",
                    )
                )

                if fb1.a6q3 == 1:
                    rows.append(
                        (
                            "a6",
                            f"Für die Versiegelung sind Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a6q4 or ''}",
                            "",
                        )
                    )
                elif fb1.a6q3 == 2:
                    rows.append(
                        (
                            "a6",
                            "",
                            f"Für die Versiegelung sind keine Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a6q5 or ''}",
                        )
                    )

            # a7: Klimaschädliche Wirkung
            if fb1.a7q1 == 1:
                rows.append(
                    (
                        "a7",
                        "",
                        f"Das Vorhaben hat folgende klimaschädliche Wirkung: {fb1.a7q2 or ''}",
                    )
                )

            # a8: Klimaschützende Wirkung
            if fb1.a8q1 == 1:
                rows.append(
                    (
                        "a8",
                        f"Das Vorhaben hat folgende klimaschützende / Klimaresilienz fördernde Wirkung: {fb1.a8q2 or ''}",
                        "",
                    )
                )

        # FB2 - Fragebogen B
        fb2 = eingabe.fb2 if eingabe.f2 else None
        if fb2:
            if fb2.b1q1 == 1:
                # b1: B-Plan Festsetzungen
                if fb2.b1q2 == 1:
                    rows.append(
                        ("b1", "Im B-Plan wurde eine PV-Pflicht verankert.", "")
                    )
                elif fb2.b1q2 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine PV-Pflicht verankert. Erläuterung: {fb2.b1q3 or ''}",
                        )
                    )

                if fb2.b1q4 == 1:
                    rows.append(
                        ("b1", "Im B-Plan wurde eine Gründachpflicht verankert.", "")
                    )
                elif fb2.b1q4 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine Gründachpflicht verankert. Erläuterung: {fb2.b1q5 or ''}",
                        )
                    )

                if fb2.b1q6 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurde eine nachhaltige Regenwasserbewirtschaftung verankert. Erläuterung: {fb2.b1q7 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q6 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine nachhaltige Regenwasserbewirtschaftung verankert. Erläuterung: {fb2.b1q8 or ''}",
                        )
                    )

                if fb2.b1q9 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden weitere wasserrückhaltende Maßnahmen verankert. Erläuterung: {fb2.b1q10 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q9 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurden keine weiteren wasserrückhaltende Maßnahmen verankert. Erläuterung: {fb2.b1q11 or ''}",
                        )
                    )

                if fb2.b1q12 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden weitere hitzepräventive Maßnahmen verankert. Erläuterung: {fb2.b1q13 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q12 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurden keine weiteren hitzepräventive Maßnahmen verankert. Erläuterung: {fb2.b1q14 or ''}",
                        )
                    )

                if fb2.b1q15 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden ein Fokus auf platzsparendes Bauen gelegt. Erläuterung: {fb2.b1q16 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q15 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurden kein Fokus auf platzsparendes Bauen gelegt und möglichst wenig Fläche versiegelt. Erläuterung: {fb2.b1q17 or ''}",
                        )
                    )

                if fb2.b1q18 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan werden die Kaltluftschneisen geschützt. Erläuterung: {fb2.b1q19 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q18 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan werden die Kaltluftschneisen nicht geschützt. Erläuterung: {fb2.b1q20 or ''}",
                        )
                    )

            # b2: Konzept/Planung
            if fb2.b2q2:
                rows.append(
                    (
                        "b2",
                        f"Durch das Vorhaben können indirekt positive Auswirkungen auf physische Maßnahmen mit Klimawirkung entstehen. Erläuterung: {fb2.b2q2}",
                        "",
                    )
                )
            if fb2.b2q3:
                rows.append(
                    (
                        "b2",
                        "",
                        f"Durch das Vorhaben können indirekt negative Auswirkungen auf physische Maßnahmen mit Klimawirkung entstehen. Erläuterung: {fb2.b2q3}",
                    )
                )
            if fb2.b2q4 == 1 and fb2.b2q5:
                rows.append(
                    (
                        "b2",
                        f"Dabei wurden folgende Nachhaltigkeitskriterien beachtet: {fb2.b2q5}",
                        "",
                    )
                )

        # FB3 - Fragebogen C
        fb3 = eingabe.fb3 if eingabe.f3 else None
        if fb3:
            # c1: Positive Beeinflussung
            if fb3.c1q1 == 1:
                if fb3.c1q2 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird das Konsumverhalten klimapositiv beeinflusst. Erläuterung: {fb3.c1q3 or ''}",
                            "",
                        )
                    )
                if fb3.c1q4 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird die Mobilität klimapositiv beeinflusst. Erläuterung: {fb3.c1q5 or ''}",
                            "",
                        )
                    )
                if fb3.c1q6 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird das Wissen über Klimaschutz oder Klimaanpassung positiv beeinflusst. Erläuterung: {fb3.c1q7 or ''}",
                            "",
                        )
                    )
                if fb3.c1q8 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird klimarelevantes Verhalten positiv beeinflusst. Erläuterung: {fb3.c1q9 or ''}",
                            "",
                        )
                    )

            # c2: Negative Beeinflussung
            if fb3.c2q1 == 1:
                if fb3.c2q2 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird das Konsumverhalten klimanegativ beeinflusst. Erläuterung: {fb3.c2q3 or ''}",
                        )
                    )
                if fb3.c2q4 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird die Mobilität klimanegativ beeinflusst. Erläuterung: {fb3.c2q5 or ''}",
                        )
                    )
                if fb3.c2q6 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird das Wissen über Klimaschutz oder Klimaanpassung negativ beeinflusst. Erläuterung: {fb3.c2q7 or ''}",
                        )
                    )
                if fb3.c2q8 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird klimarelevantes Verhalten negativ beeinflusst. Erläuterung: {fb3.c2q9 or ''}",
                        )
                    )

        # FB4 - Fragebogen D
        fb4 = eingabe.fb4 if eingabe.f4 else None
        if fb4:
            if fb4.d1q1:
                rows.append(
                    (
                        "d1",
                        f"Das Vorhaben hat folgende positive Klimarelevanz: {fb4.d1q1}",
                        "",
                    )
                )

            if fb4.d2q1:
                rows.append(
                    (
                        "d2",
                        "",
                        f"Das Vorhaben hat folgende negative Klimarelevanz: {fb4.d2q1}",
                    )
                )

        return rows

    def _export_fb5(self, f5: bool):
        """Export Fragebogen F (f5) - Keine Klimawirksamkeit"""
        if not f5:
            return

        self.set_font("free-sans", "B", 12)
        self.cell(
            0, 8, "Fragebogen F: Keine Klimawirksamkeit", new_x="LMARGIN", new_y="NEXT"
        )
        self.set_font("free-sans", "", 10)
        self.cell(
            0,
            6,
            "Das Vorhaben ist in keiner Weise klimawirksam.",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(5)

    def export(self, eingabe: KlimarelevanzpruefungEingabe):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()

        # Title
        self.set_font("free-sans", "B", 14)
        self.cell(
            0,
            6,
            f'Klimarelevanzprüfung zur Vorlage „{eingabe.magistratsvorlage.name}"',
            border=False,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_font("free-sans", "", 14)
        self.cell(
            0,
            6,
            f"Vorlagennummer: {eingabe.magistratsvorlage.verwaltungsvorgang_nr}",
            border=False,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(10)

        # Collect all rows and export as single table
        rows = self._collect_all_rows(eingabe)

        if rows:
            self._add_table_header()

            num_col_width = 10
            content_col_width = (self.w - 20 - num_col_width) / 2
            x_num = self.l_margin
            x_end = self.l_margin + num_col_width + 2 * content_col_width

            prev_group = None
            group_num = 0
            group_y_start = None
            group_y_end = None

            for i, (group, positive_text, negative_text) in enumerate(rows):
                is_new_group = prev_group != group
                is_last_row = i == len(rows) - 1
                next_group = rows[i + 1][0] if not is_last_row else None
                is_last_in_group = is_last_row or next_group != group

                # Increment group number and reset y tracking when group changes
                if is_new_group:
                    group_num += 1
                    group_y_start = self.get_y()

                draw_top_border = prev_group is not None and prev_group != group
                y_start, y_end, _ = self._add_table_row(
                    group_num,
                    positive_text,
                    negative_text,
                    draw_top_border,
                    show_number=False,
                )
                group_y_end = y_end

                # Draw number when group ends (either last row or next row is different group)
                if is_last_in_group:
                    self._draw_group_number(
                        group_num, group_y_start, group_y_end, num_col_width
                    )

                prev_group = group

            # Draw final bottom border for the entire table
            if group_y_end is not None:
                self.set_line_width(0.2)
                self.set_draw_color(0, 0, 0)
                self.line(x_num, group_y_end, x_end, group_y_end)

        self.ln(5)

        # Export F5 separately (no climate relevance)
        if eingabe.f5:
            self._export_fb5(eingabe.f5)

        # Create a bytes buffer to save the PDF
        pdf_output = BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output
