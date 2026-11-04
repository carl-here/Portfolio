package edu.ntnu.iir.bidata;

import java.util.HashMap;

/**
 *Klassen.
 *
 * @author Charlotte Hjort
 * @version 2026.10.27
 * @return det som blir skrevet inn
 */

public class AktivitetsRegister {

  /**
   *Lagrer aktivitetene laget i et HashMap slik at søk er lettere.
   */
  private HashMap<String, Aktivitet> aktiviteter;

  /**
   *Lagrer nytt hashmap HashMap slik at søk er lettere.
   */
  public AktivitetsRegister() {
    this.aktiviteter = new HashMap<>();
  }

  /**
   *Registrer til en aktivitet i registeret.
   */
  public void registrerAktivitet(Aktivitet aktivitet) {
    aktiviteter.put(aktivitet.getTypeAktivitet(), aktivitet);
  }

  /**
   *Søke etter en aktivitet.
   */
  public Aktivitet finnAktivitet(String typeAktivitet) {
    return aktiviteter.get(typeAktivitet);
  }

  /**
   * Boolean for å slette.
   */
  public boolean slettAktivitet(String typeAktivitet) {
    if (aktiviteter.containsKey(typeAktivitet)) {
      aktiviteter.remove(typeAktivitet);
      return true;
    }
    return false;
  }

  /**
   * Get metode for skrive ut alle aktivitetene.
   */
  public HashMap<String, Aktivitet> getAlleAktiviteter() {
    return aktiviteter;
  }
}
