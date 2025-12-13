# ---------- OPPONENT'S TURN PHASES -----------
def defenseScreen(
    svSuccessCtr: int,
    svCritCtr: int,
    failedSvs: int,
    opponentHits: int,
    opponentCrits: int,
    opponentSuccess: int
):
    print(f"THE OPPONENT SCORED [{opponentSuccess}] HITS ON YOUR OPERATIVE! OF WHICH:")
    if opponentHits != 0:
        print(f"    [{opponentHits}] WERE NORMAL SUCCESSFUL HITS!")
    if opponentCrits != 0:
        print(f"    [{opponentCrits}] WERE SUCCESSFUL CRITIAL HITS!")

    print("===--------------------------===")

    print(f"YOU'VE SUCCESFULLY ROLLED: ")
    if svSuccessCtr != 0:
        print(f"    [{svSuccessCtr}] NORMAL SAVES!" )

    if svCritCtr != 0:
        print(f"    [{svCritCtr}] CRITICAL SAVES!" )

    # Initialize remaining values
    remainingHits = opponentHits
    remainingCrits = opponentCrits
    remainingSvSuccess = svSuccessCtr
    remainingSvCrit = svCritCtr


    if opponentHits != 0 and opponentCrits != 0 and svCritCtr == 0 and svSuccessCtr == 0 and failedSvs == 3:
        print(f"!!!YOU'VE FAILLED ALL 3 SAVES! NO ACTION CAN BE TAKEN!!! \n >>> YOUR OPPONENT HITS YOU WITH [{opponentHits}] NORMAL HIT AND [{opponentCrits}] CRITICAL HITS! <<<")    
        return remainingHits, remainingCrits, 0, 0

    while True:
        opts = [] # Intialiuze option list

        # Opt 1. Using Normal saves to block Normal Hits (Scenarios B2, C2, D2, E2; B3, C3, D3)
        if remainingHits > 0 and remainingSvSuccess > 0:
            canBlock = min(remainingHits, remainingSvSuccess)
            opts.append({
                "text": f"USE [{canBlock}] NORMAL SAVE(S) TO SAVE [{canBlock}] OPPONENT'S  SUCCESSFUL HIT(S)",
                "type": "normal-vs-normal",
                "amount": canBlock
            })

        # Opt 2. Using Crit saves to block Crit Hits (Scenarios C3, D3, E3; C4, D4, E4)
        if remainingCrits > 0 and remainingSvCrit > 0:
            canBlock = min(remainingCrits, remainingSvCrit)
            opts.append({
                "text": f"USE [{canBlock}] CRIT SAVE(S) TO SAVE [{canBlock}] OF OPPONENT'S CRIT HIT(S)",
                "type": "crit-vs-crit",
                "amount": canBlock
            })
            

        # Opt 3. Using Normal saves to block Crit Hits (Scenarios C3, D3; C4, D4)
        if remainingCrits > 0 and remainingSvSuccess >= 2:
            canBlock = min(remainingCrits, remainingSvSuccess // 2)
            opts.append({
                "text": f"USE [{canBlock * 2}] NORMAL SAVES TO SAVE [{canBlock}] OF OPPONENT'S CRIT HIT",
                "type": "normal-vs-crit",
                "amount": canBlock
            })

        # Opt 4. Using Crit saves to block normal Hits (Scenarios: C2, D2, E2; E3)
        if remainingHits > 0 and remainingSvCrit > 0:
            canBlock = min(remainingHits, remainingSvCrit)
            opts.append({
                "text": f"USE [{canBlock}] CRIT SAVE(S) TO SAVE [{canBlock}] OF OPPONENT'S SUCCESSFUL HIT(S)",
                "type": "crit-vs-normal",
                "amount": canBlock
            })

        # If no options available, exit
        if not opts:
            print("\n>>> NO MORE SAVES AVAILABLE <<<")
            break

        # print("YOU CAN:")
        # # if both player and opponent only have normal saves and hit rolls respectively
        # if opponentHits != 0 and svSuccessCtr != 0:
        #     opts.append(f" USE YOUR [{svSuccessCtr}] NORMAL SAVES TO SAVE THAT {svSuccessCtr} OF OPPONENT'S [{opponentHits}] SUCCESSFUL HITS")
        # # if both player and opponent have crit saves and crit hit respectively 
        
        # if opponentCrits != 0  and svCritCtr != 0:
        #     opts.append(f" USE YOUR [{svCritCtr}] CRIT SAVES TO SAVE {svCritCtr} OF OPPONENT'S [{opponentCrits}] CRITICAL HITS")

        # # if player does not have any crit saves to save opponent crit hits
        # if opponentCrits != 0 and svCritCtr == 0 and svSuccessCtr != 0 and svSuccessCtr >= 2:
        #     critSave = math.floor(svSuccessCtr/2) # Rounded down result
        #     opts.append(f" USE 2 OF YOUR [{svSuccessCtr}] NORMAL SAVES TO SAVE [{critSave}] NUMBER OF OPPONENT'S [{opponentCrits}] CRITICAL HITS")

        # If no options available, exit
        if not opts:
            print("\n>>> NO MORE SAVES AVAILABLE <<<")
            break

        print("Xxx ---------------- xxX")
        for i, option in enumerate(opts, 1):
            print(f"{i}.{option["text"]}")
        print(f"{len(opts) + 1}. DONE (STOP USING SAVES)")
        print("Xxx ---------------- xxX")

        while True:
            try:
                # print(len(opts))
                choice = int(input(">>> "))

                # Check if player wants to stop
                if choice == len(opts) + 1:
                    print("\n>>> PLAYER CHOSE TO STOP <<<")
                    break

                if 1 <= choice <= len(opts):
                    selected = opts[choice - 1]

                    if selected["type"] == "normal-vs-normal":
                        amount = selected["amount"]
                        remainingHits -= amount
                        remainingSvSuccess -= amount
                        print(f"\n--- BLOCKED [{amount}] NORMAL HIT(S) WITH [{amount}] NORMAL SAVE(S) ---")

                    elif selected["type"] == "crit-vs-crit":
                        amount = selected["amount"]
                        remainingCrits -= amount
                        remainingSvCrit -= amount
                        print(f"\n--- BLOCKED [{amount}] CRIT HIT(S) WITH [{amount}] CRIT SAVE(S) ---")

                    elif selected["type"] == "normal-vs-crit":
                        amount = selected["amount"]
                        remainingCrits -= amount
                        remainingSvSuccess -= (amount * 2)
                        print(f"\n--- BLOCKED [{amount}] CRIT HIT(S) WITH [{amount * 2}] NORMAL SAVE(S) ---")

                    elif selected["type"] == "crit-vs-normal":
                        amount = selected["amount"]
                        remainingHits -= amount
                        remainingSvCrit -= amount
                        print(f"\n--- BLOCKED [{amount}] NORMAL HIT(S) WITH [{amount}] CRIT SAVE(S) ---")

                    # Updated debug message
                    print(f"[DEBUG] Remaining - Hits: {remainingHits} | Crits: {remainingCrits} | SvSuccess: {remainingSvSuccess} | SvCrit: {remainingSvCrit}")
                    break
                else:
                    print("INVALID OPTION!")
            except ValueError:
                print("Please input a number!")
          
        # Check if player chose to stop
        if choice == len(opts) + 1:
            break
    
    # Final summary
    print("\n===--------------------------===")
    print("FINAL RESULTS:")
    print(f"  OPPONENT HITS THAT GOT THROUGH: [{remainingHits}] NORMAL, [{remainingCrits}] CRIT")
    print(f"  UNUSED SAVES: [{remainingSvSuccess}] NORMAL, [{remainingSvCrit}] CRIT")
    print("===--------------------------===")
    
    # Only return these 2 values, unused saves whehter normal or crits will be discarded
    return remainingHits, remainingCrits


def damageAllocation(
    hits: int,
    crits: int,
    # opProfile: dict
    testOperativeHP: int,
    testOpponentDmg: int,
    testOpponentCrit: int
):
    if hits != 0 or crits != 0:
        if hits > 0:
            normalDmgDealt = testOpponentDmg * hits
            testOperativeHP -= normalDmgDealt
            print(f"----- OPPONENT DEALT {normalDmgDealt} DAMAGE TO OPERATIVE! ----- ")

        if crits > 0:
            critDmgDealt = testOpponentCrit * crits
            testOperativeHP -= critDmgDealt
            print(f"----- OPPONENT DEALT {critDmgDealt} DAMAGE TO OPERATIVE! ----- ")
    else:
        print("----- No Damage dealt to Operative! -----")

    # Prevent negative HP
    testOperativeHP = max(0, testOperativeHP)

    return testOperativeHP