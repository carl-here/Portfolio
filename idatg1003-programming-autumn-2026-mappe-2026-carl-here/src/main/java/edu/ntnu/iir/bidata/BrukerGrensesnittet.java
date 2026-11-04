package edu.ntnu.iir.bidata;

/**
 * Klassen InputLeser skal lese det en bruker skriver inn,
 * den skal kunne kalles på for å lese input.
 * Klassen håndterer all inputdata og kan kalles av andre klasser.
 * Dette gir sterkere kobling (coupling) mellom klasser, men er
 * nødvendig for å ha en ryddig og sammenhengende (cohesiant).
 * Den har tre get metoder: en for å hente inn tekst/strings, en
 * for dato, og en for integers.
 *
 * @author Charlotte Hjort
 * @version 2026.10.27
 * @return det som blir skrevet inn
 */

public class BrukerGrensesnittet {
  InputLeser leser = new InputLeser();
  private AktivitetsRegister registrerteaktiviteter = new AktivitetsRegister();

  /**
   *Starter programmet.
   */
  public void start() {
    int valg;
    do {
      System.out.println("\nAktivitets Meny");
      System.out.println("Trykk 1 for å legge til en aktivitet");
      System.out.println("Trykk 2 for å se alle aktiviteter registrert");
      System.out.println("Trykk 3 for å søke etter en aktivitet");
      System.out.println("Trykk 4 for å slette en aktivitet");
      System.out.println("Trykk 0 for å avslutte NB: da blir alt blir sletta!");

      valg = leser.getIntInput("").orElse(-1);

      switch (valg) {
        case 1 -> leggTilAktivitet();
        case 2 -> skrivUtAlleAktiviteter();
        case 3 -> sokEtterAktivitet();
        case 4 -> slettAktivitet();
        default -> System.out.println("Du kan ikke skrive det!");
      }
    } while (valg != 0);
  }

  /**
   *Legger inn ui for input av aktivitet.
   */
  public void leggTilAktivitet() {
    Aktivitet aktivitet = new Aktivitet(
        leser.getTekstInput("\nSkriv inn type aktivitet: "),
        leser.getTekstInput("Skriv inn aktivitetsansvarlig: "),
        leser.getIntInput("Skriv inn antall deltakere (teller): ").orElse(0),
        leser.getTekstInput("Skriv inn sted: "),
        leser.getDateInput("Skriv inn på formatet 2026-11-02:")
    );
    registrerteaktiviteter.registrerAktivitet(aktivitet);
    System.out.println("Aktivitet registert!");
    System.out.println(aktivitet); // Bruk toString () i Aktivitet for utskrift

  }

  /**
   *  Under er metoder som bruker logikken fra aktivitetsregisteret.
   */
  private void skrivUtAlleAktiviteter() {
    System.out.println("\n--- Alle aktiviteter ---");
    if (registrerteaktiviteter.getAlleAktiviteter().isEmpty()) {
      System.out.println("Ingen aktiviteter registrert.");
    } else {
      registrerteaktiviteter.getAlleAktiviteter().values().forEach(System.out::println);
    }
  }

  private void sokEtterAktivitet() {
    String typeAktivitet = leser.getTekstInput("Skriv inn aktivitetsansvarlig: ");
    Aktivitet funnetAktivitet = registrerteaktiviteter.finnAktivitet(typeAktivitet);

    if (funnetAktivitet != null) {
      System.out.println("Vi fant: " + funnetAktivitet);
    } else {
      System.out.println("Ingen aktiviteter ved det navnet funnet.");
    }
  }

  private void slettAktivitet() {
    String typeAktivitet = leser.getTekstInput("Skriv inn hvilken  aktivitet du vil slette: ");
    boolean slettet = registrerteaktiviteter.slettAktivitet(typeAktivitet);

    if (slettet) {
      System.out.println("Aktivitet" + typeAktivitet + " slettet.");
    } else {
      System.out.println("Ingen aktiviteter ved det navnet funnet.");
    }
  }
}
