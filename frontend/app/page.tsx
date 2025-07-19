import InvoiceUpload from "@/components/invoice";
import Image from "next/image";

export default function Home() {
  return (
    <InvoiceUpload onFilesSelected={(files) => console.log(files)} />
  );
}
