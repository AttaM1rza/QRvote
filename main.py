import argparse
import os

from config_detection_strategies import detection_strategies
from qrvote import QRvote


def register_voter(id, name):
    _, qr_code_path = QRvote.create_voting_qr_code(id, name)
    pdf_output_file = QRvote.create_voting_qr_code_pdf(qr_code_path, id, name)
    os.system(f'open "{pdf_output_file}"')
    print(f"QR code created for {name} with ID number {id}.")


def start_voting(sources, strategy_name):
    strategy = detection_strategies.get(strategy_name)
    qrvote = QRvote(sources=sources, detection_strategy=strategy)
    qrvote.detect_votes_from_camera_stream()


def main():
    parser = argparse.ArgumentParser(description="QRvote CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    register_parser = subparsers.add_parser("register", help="Register a voter")
    register_parser.add_argument("--id", required=True, help="Jamaat ID-number")
    register_parser.add_argument("--name", required=True, help="Voter name")

    vote_parser = subparsers.add_parser("vote", help="Start the voting process")
    vote_parser.add_argument(
        "--sources",
        help="Comma-separated list of camera IDs (ex. 0,1,2) or file paths (ex. videos/sample.mp4). By default, the laptop camera is 0.",
        default="0",
    )
    vote_parser.add_argument(
        "--strategy",
        help=f"Used Detection strategy. Currently available: {', '.join(detection_strategies.keys())}",
        default=list(detection_strategies.keys())[0],
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "register":
        register_voter(args.id, args.name)
    elif args.command == "vote":
        sources = [int(s) if s.isdigit() else s for s in args.sources.split(",")]
        start_voting(sources, args.strategy)


if __name__ == "__main__":
    main()
