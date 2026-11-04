package edu.ntnu.iir.bidata;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

class AktivitetsMenyTest {
  @Test
  public void testLeggTilAktivitet() {
    // Positive test: Legg til en aktivitet og sjekk at den blir registrert
    AktivitetsRegister register = new AktivitetsRegister();
    Aktivitet aktivitet = new Aktivitet(
        "Fotball",
        "Ola Nordmann",
        10,
        "Parken",
        LocalDate.of(2026, 11, 5)
    );

    register.registrerAktivitet(aktivitet);
    assertEquals(1, register.getAlleAktiviteter().size());
    assertTrue(register.getAlleAktiviteter().containsKey("Fotball-10"));
  }

  @Test
  public void testSokEtterAktivitet() {
    // Positive test: Søk etter en aktivitet som eksisterer
    AktivitetsRegister register = new AktivitetsRegister();
    Aktivitet aktivitet = new Aktivitet(
        "Sang",
        "Kari Hansen",
        15,
        "Kultursalen",
        LocalDate.of(2026, 12, 10)
    );

    register.registrerAktivitet(aktivitet);
    Aktivitet funnetAktivitet = register.finnAktivitet("Sang");

    assertNotNull(funnetAktivitet);
    assertEquals("Kari Hansen", funnetAktivitet.getAktivitetsansvarlig());
  }

  @Test
  public void testSlettAktivitet() {
    // Positive test: Slett en aktivitet og sjekk at den blir fjernet
    AktivitetsRegister register = new AktivitetsRegister();
    Aktivitet aktivitet = new Aktivitet(
        "Fotball",
        "Ola Nordmann",
        10,
        "Parken",
        LocalDate.of(2026, 11, 5)
    );

    register.registrerAktivitet(aktivitet);
    boolean slettet = register.slettAktivitet("Fotball");

    assertTrue(slettet);
    assertEquals(0, register.getAlleAktiviteter().size());
  }

  @Test
  public void testSokEtterIkkeEksisterendeAktivitet() {
    // Negative test: Søk etter en aktivitet som ikke eksisterer
    AktivitetsRegister register = new AktivitetsRegister();
    Aktivitet funnetAktivitet = register.finnAktivitet("IkkeEksisterende");

    assertNull(funnetAktivitet);
  }

  @Test
  public void testSlettIkkeEksisterendeAktivitet() {
    // Negative test: Prøv å slette en aktivitet som ikke eksisterer
    AktivitetsRegister register = new AktivitetsRegister();
    boolean slettet = register.slettAktivitet("IkkeEksisterende");

    assertFalse(slettet);
  }

}