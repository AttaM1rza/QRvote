import os

from qrvote import QRvote


def registration_process():
    """
    This function should handle the registration of voters and create a QR code for each registered voter.
    """
    print("Registration process started...")
    id_number = input("Enter voters ID-number: ")
    name = input("Enter voters name: ")
    print("Creating QR code...")
    if not id_number.isdigit() or not name:
        print("Invalid ID number. Please enter a valid number.")
        return
    _, qr_code_path = QRvote.create_voting_qr_code(id_number, name)
    # TODO make the qr_code printable
    #      add to it the ID number and name ...
    pdf_output_file = QRvote.create_voting_qr_code_pdf(qr_code_path, id_number, name)
    os.system(f'open "{pdf_output_file}"')
    print(f"QR code created for {name} with ID number {id_number}.")


def voting_process():
    """
    This function should handle the voting process and detect QR codes from the camera stream.
    """
    sources = input("Enter sources seperated by comma (sources can be camera-id's or filepath's): ")
    # TODO UNCOMMENT THIS (FOR TESTING PURPOSES ONLY)
    # sources = dummy_camera_stream_1 + "," + dummy_camera_stream_2
    # sources = dummy_camera_stream_little_1
    if not sources:
        print("No sources provided. Exiting...")
        return
    sources = sources.split(",")
    sources = [int(source) if source.isdigit() else source for source in sources]
    qrvote = QRvote(sources=sources)
    qrvote.detect_votes_from_camera_stream()


def main():
    while True:
        print("\n" * 10, "QRvote Main Menu")
        print("1. Register a voter")
        print("2. Start voting process")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            registration_process()
        elif choice == "2":
            voting_process()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

    return


if __name__ == "__main__":
    main()
