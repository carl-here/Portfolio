package edu.ntnu.iir.bidata;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

/**
 * Klassen Aktivitet tar inn
 * detaljer om parameterene aktiviteten registrert.
 */
public class Aktivitet {
  private String typeAktivitet;
  private String aktivitetsansvarlig;
  private int teller;
  private String sted;
  private LocalDate tid;

  /**
   * Logg detaljer om hva slags aktiviteter som registreres.
   *
   * @param typeAktivitet       selvforklarende
   * @param aktivitetsansvarlig hvem er ansvarlig for arrangementet
   * @param teller              skal telle antall av hver aktivitet, nyttig for stream
   * @param sted                hvor skal aktiviteten ta plass
   * @param tid                 når skal aktiviteten ta plass
   */

  public Aktivitet(String typeAktivitet,
                   String aktivitetsansvarlig,
                   int teller,
                   String sted,
                   LocalDate tid) {
    this.typeAktivitet = typeAktivitet;
    this.aktivitetsansvarlig = aktivitetsansvarlig;
    this.teller = teller;
    this.sted = sted;
    this.tid = tid;
  }

  public String getTypeAktivitet() {
    return typeAktivitet;
  }

  public String getAktivitetsansvarlig() {
    return aktivitetsansvarlig;
  }

  public int getTeller() {
    return teller;
  }

  public String getSted() {
    return sted;
  }

  public LocalDate getTid() {
    return tid;
  }

  /**
   *Brukervennlig utskrift  for å få bekreftet at noe skjedde etter input.
   */
  @Override
  public String toString() {
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    return "~~~~~~~~~~ Aktivitet Registrert!  ~~~~~~~~"
        + "\n◦ Type: " + typeAktivitet
        + "\n◦ Ansvarlig: " + aktivitetsansvarlig
        + "\n◦ Deltakere: " + teller
        + "\n◦ Sted: " + sted
        + "\n◦ Tid: " + tid.format(formatter);
  }
}
