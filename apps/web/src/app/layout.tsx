import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Sotto Salon",
  description:
    "Subscription-funded directory for verified adults to publish moderated profile advertisements in approved jurisdictions.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body
        style={{
          fontFamily: "system-ui, sans-serif",
          margin: 0,
          padding: "2rem",
          lineHeight: 1.5,
        }}
      >
        {children}
      </body>
    </html>
  );
}
