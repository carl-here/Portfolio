package edu.ntnu.iir.bidata;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Optional;
import java.util.Scanner;

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

public class InputLeser {
  private Scanner leser;

  /**
   *Lager en konstruktør.
   */
  public InputLeser() {
    leser = new Scanner(System.in);
  }

  /**
   *Spør brukeren om en heltallsverdi.
   *
   *@param prompt Teksten som vises til brukeren.
   *@return Heltallsverdien fra brukeren.
   */
  public String getTekstInput(String prompt) {
    System.out.print(prompt);
    return leser.nextLine().trim();
  }

  /**
   * DateTime funksjon for å hente dato.
   */
  public LocalDate getDateInput(String prompt) {
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    LocalDate dato = null;

    while (dato == null) {
      System.out.println(prompt);
      String input = leser.nextLine().trim();

      try {
        dato = LocalDate.parse(input, formatter);
      } catch (DateTimeParseException e) {
        System.out.println("ugjyldig format...");
      }
    }
    return dato;
  }

  /**
   *Integer logikk henting.
   */
  public Optional<Integer> getIntInput(String prompt) {
    System.out.print(prompt);
    if (leser.hasNextInt()) {
      int value = leser.nextInt();
      leser.nextLine(); // Tøm bufferen
      return Optional.of(value); // Returner Optional med verdien
    } else {
      leser.nextLine(); // Tøm bufferen for å unngå uendelig loop
      System.out.println("Du kan ikke skrive det! Prøv igjen.");
      return Optional.empty(); // Returner tom Optional ved feil
    }
  }
}

